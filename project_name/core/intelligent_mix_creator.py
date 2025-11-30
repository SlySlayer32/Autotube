import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from pydub import AudioSegment  # Required for mix generation

from .analysis_pipeline import AudioAnalysisPipeline
from .audio_metadata import AudioAnalysisData, AudioMetadata
from .mix_creator import MixCreator  # Assuming MixCreator is in the same directory

logger = logging.getLogger(__name__)


class IntelligentMixCreator(MixCreator):
    """Enhanced MixCreator with intelligent audio analysis integration"""

    def __init__(
        self, output_folder: str = "output_mixes"
    ):  # Added output_folder to super()
        super().__init__(output_folder=output_folder)  # Pass output_folder to parent
        self.analysis_pipeline = AudioAnalysisPipeline()
        self.analyzed_clips: Dict[
            str, AudioMetadata
        ] = {}  # Store by file_path as string

    def add_clip_with_analysis(
        self, file_path: Path, force_reanalysis: bool = False
    ) -> Optional[AudioMetadata]:
        """Add clip and perform analysis, storing it."""
        try:
            metadata = self.analysis_pipeline.analyze_audio_file(
                file_path, force_reanalysis=force_reanalysis
            )
            self.analyzed_clips[str(file_path)] = metadata
            logger.info(f"Analyzed and cached metadata for {file_path}")
            return metadata
        except Exception as e:
            logger.error(f"Failed to analyze or add clip {file_path}: {e}")
            return None

    def create_intelligent_mix(  # Renamed for clarity, more generic
        self,
        clip_paths: List[Path],
        mix_type: str = "sleep",  # sleep, focus, relax
        target_duration_minutes: int = 60,
        sleep_phase: Optional[str] = None,  # Specific to sleep mixes
        add_binaural_beats: bool = False,  # from parent
        binaural_base_freq: float = 200.0,  # from parent
        binaural_beat_freq: float = 5.0,  # from parent
    ) -> Optional[Path]:
        """Create mix using intelligent analysis based on mix_type."""

        analyzed_clips_data: List[AudioMetadata] = []
        for path in clip_paths:
            path_str = str(path)
            if path_str not in self.analyzed_clips:
                meta = self.add_clip_with_analysis(path)
                if meta:
                    analyzed_clips_data.append(meta)
            else:
                analyzed_clips_data.append(self.analyzed_clips[path_str])

        if not analyzed_clips_data:
            logger.warning(
                "No clips available for intelligent mix creation after analysis."
            )
            return None

        # Select and weight clips based on metrics
        # The selection criteria will vary based on mix_type
        if mix_type == "sleep":
            selected_clips_with_scores = self._select_clips_for_sleep(
                analyzed_clips_data, sleep_phase or "falling_asleep"
            )
        elif mix_type == "focus":
            selected_clips_with_scores = self._select_clips_for_focus(
                analyzed_clips_data
            )
        elif mix_type == "relax":
            selected_clips_with_scores = self._select_clips_for_relax(
                analyzed_clips_data
            )
        else:
            logger.warning(
                f"Unknown mix_type: {mix_type}. Defaulting to generic selection."
            )
            # Fallback: select based on a generic score or just take top N
            selected_clips_with_scores = [
                (clip, 0.5) for clip in analyzed_clips_data[:8]
            ]

        if not selected_clips_with_scores:
            logger.warning(f"No suitable clips found for mix_type '{mix_type}'.")
            return None

        # Create intelligent layering/mix plan
        # This part is highly conceptual and needs detailed design.
        # For now, we'll just pass the selected file paths to the parent's create_mix.
        # A true intelligent mix plan would define start times, durations, volumes, effects per clip.

        # Simplified: Create a dictionary for the parent create_mix method
        # We need to categorize them first, or adapt create_mix to take a list of AudioMetadata

        # For now, let's just use the file paths of selected clips and a default category "intelligent_mix"
        # This bypasses the category-based mixing of the parent for a simpler intelligent flow.
        # A more advanced approach would be to create a "mix_plan" object.

        # Construct audio_files dict for parent create_mix
        # This is a temporary adaptation. Ideally, parent create_mix would be more flexible.
        intelligent_audio_files: Dict[str, List[str]] = {"selected_for_mix": []}
        for metadata, score in selected_clips_with_scores:
            intelligent_audio_files["selected_for_mix"].append(str(metadata.file_path))

        if not intelligent_audio_files["selected_for_mix"]:
            logger.warning(
                "No clips selected for the intelligent mix based on criteria."
            )
            return None

        # Use parent's create_mix for actual audio generation with selected files
        # We are passing a single category here. The parent's logic will pick from this.
        # This is a simplification. A more robust solution would involve a more detailed mix plan.
        output_path_str = super().create_mix(
            audio_files=intelligent_audio_files,  # Pass the selected files
            mix_type=mix_type,  # Pass through mix_type for effects
            duration_minutes=target_duration_minutes,
            add_binaural_beats=add_binaural_beats,
            binaural_base_freq=binaural_base_freq,
            binaural_beat_freq=binaural_beat_freq,
        )

        if output_path_str:
            logger.info(f"Created intelligent {mix_type} mix: {output_path_str}")
            return Path(output_path_str)
        return None

    def _select_clips_for_sleep(
        self, clips: List[AudioMetadata], sleep_phase: str
    ) -> List[Tuple[AudioMetadata, float]]:
        """Select and score clips for sleep mix"""
        scored_clips = []
        for clip_meta in clips:
            if not clip_meta.analysis:
                logger.debug(
                    f"Skipping clip {clip_meta.file_path} due to missing analysis data."
                )
                continue

            analysis_data = clip_meta.analysis
            score = self._calculate_sleep_suitability_score(analysis_data, sleep_phase)

            if score > 0.3:  # Minimum threshold
                scored_clips.append((clip_meta, score))

        scored_clips.sort(key=lambda x: x[1], reverse=True)
        logger.info(
            f"Selected {len(scored_clips)} clips for sleep phase '{sleep_phase}' based on scores."
        )
        return scored_clips[:8]  # Limit to top N clips

    def _select_clips_for_focus(
        self, clips: List[AudioMetadata]
    ) -> List[Tuple[AudioMetadata, float]]:
        scored_clips = []
        for clip_meta in clips:
            if not clip_meta.analysis:
                continue
            analysis = clip_meta.analysis
            # Prioritize focus_enhancement_score, low arousal, moderate valence
            score = (
                analysis.focus_enhancement_score * 0.5
                + (1 - analysis.arousal) * 0.3  # Low arousal is good for focus
                + (1 - abs(analysis.valence - 0.5))
                * 0.2  # Neutral to slightly positive valence
            )
            if score > 0.3:
                scored_clips.append((clip_meta, score))
        scored_clips.sort(key=lambda x: x[1], reverse=True)
        return scored_clips[:8]

    def _select_clips_for_relax(
        self, clips: List[AudioMetadata]
    ) -> List[Tuple[AudioMetadata, float]]:
        scored_clips = []
        for clip_meta in clips:
            if not clip_meta.analysis:
                continue
            analysis = clip_meta.analysis
            # Prioritize relaxation_factor, low arousal, positive valence
            score = (
                analysis.relaxation_factor * 0.5
                + (1 - analysis.arousal) * 0.3
                + analysis.valence * 0.2  # Positive valence
            )
            if score > 0.3:
                scored_clips.append((clip_meta, score))
        scored_clips.sort(key=lambda x: x[1], reverse=True)
        return scored_clips[:8]

    def _calculate_sleep_suitability_score(
        self, analysis: AudioAnalysisData, sleep_phase: str
    ) -> float:
        """Calculate how suitable a clip is for specific sleep phase"""
        base_score = analysis.sleep_induction_potential

        phase_score_component = 0.0
        if sleep_phase == "falling_asleep":
            phase_score_component = (
                analysis.relaxation_factor * 0.4
                +
                # analysis.focus_enhancement_score * 0.2 + # Focus might be counterproductive for falling asleep
                (1 - analysis.arousal) * 0.4  # Low arousal is key
                + analysis.ambient_score * 0.2
            )
        elif sleep_phase == "deep_sleep":
            phase_score_component = (
                (1 - analysis.arousal) * 0.5  # Very low arousal
                + analysis.ambient_score * 0.3  # Consistent ambient sounds
                + analysis.masking_potential * 0.2  # Good for blocking disturbances
            )
        elif sleep_phase == "rem":  # REM sleep can have more varied brain activity
            phase_score_component = (
                analysis.relaxation_factor * 0.3
                +
                # analysis.harmonic_ratio * 0.2 + # Could be too stimulating
                analysis.ambient_score * 0.4
                + (1 - analysis.arousal) * 0.3  # Still prefer lower arousal
            )
        else:  # Default to base_score if phase is unknown
            phase_score_component = base_score

        # Weighted average: base sleep potential and phase-specific suitability
        final_score = base_score * 0.6 + phase_score_component * 0.4
        return float(np.clip(final_score, 0, 1))

    def _create_sleep_mix_plan(  # This method is from the prompt but not fully used yet
        self,
        selected_clips: List[Tuple[AudioMetadata, float]],
        target_duration: float,  # Changed to float to match prompt
        sleep_phase: str,
    ) -> Dict[str, Any]:  # Changed to Dict[str, Any]
        """Create detailed mixing plan (Placeholder for now)"""

        # This would involve complex logic:
        # - Determining start/end times for each clip
        # - Volume curves
        # - Crossfade types and durations based on clip compatibility
        # - Dynamic effect application

        plan = {
            "layers": [],  # Each layer: {metadata: AudioMetadata, start_time: float, end_time: float, volume: float}
            "transitions": [],  # Each transition: {from_clip_hash: str, to_clip_hash: str, type: str, duration: float}
            "effects": [],  # Global or per-layer effects
            "target_duration": target_duration,
            "sleep_phase": sleep_phase,
            "info": "Placeholder mix plan. Advanced layering not yet implemented.",
        }

        # Simplified layering for now: sequence with crossfades
        current_time = 0.0
        for i, (clip_meta, score) in enumerate(selected_clips):
            clip_duration = (
                clip_meta.analysis.duration if clip_meta.analysis else 300
            )  # Default 5 mins

            # Adjust duration based on score or other factors (simplified)
            effective_duration = min(
                clip_duration,
                (target_duration / len(selected_clips)) * (1 + score * 0.5),
            )

            if (
                current_time + effective_duration > target_duration
                and current_time < target_duration
            ):
                effective_duration = target_duration - current_time  # Trim last clip

            if current_time >= target_duration:
                break

            plan["layers"].append(
                {
                    "file_path": str(clip_meta.file_path),
                    "start_time": current_time,
                    "duration": effective_duration,
                    "volume_db": -6 * (1 - score),  # Quieter for lower scores (example)
                }
            )

            if i > 0:
                plan["transitions"].append(
                    {
                        "from_layer_index": i - 1,
                        "to_layer_index": i,
                        "type": "crossfade",
                        "duration_ms": self.mix_profiles.get(
                            sleep_phase, self.mix_profiles["sleep"]
                        )["crossfade"],
                    }
                )
            current_time += effective_duration - (
                self.mix_profiles["sleep"]["crossfade"] / 1000 if i > 0 else 0
            )

        logger.debug(f"Generated mix plan: {plan}")
        return plan

    def _generate_intelligent_mix(self, mix_plan: Dict[str, Any]) -> Optional[Path]:
        """
        Generates the mix based on the detailed plan.
        (Placeholder - this would be a complex method replacing much of parent's create_mix)
        For now, this method is not called by create_intelligent_mix, which defers to super().create_mix
        """
        logger.info(
            f"Generating intelligent mix based on plan for sleep phase: {mix_plan.get('sleep_phase')}"
        )

        # --- This is where the advanced mixing logic would go ---
        # 1. Load all unique audio files specified in plan['layers']
        # 2. For each layer:
        #    - Get the AudioSegment
        #    - Trim/loop to layer['duration']
        #    - Apply layer['volume_db']
        # 3. Create a base AudioSegment for target_duration
        # 4. Overlay layers onto the base mix at their start_time, applying transitions
        # 5. Apply global effects
        # 6. Export the final mix

        # Simplified example: just log the plan and return a dummy path
        # In a real scenario, this would produce an actual audio file.
        dummy_output_filename = f"intelligent_mix_{mix_plan.get('sleep_phase', 'default')}_{int(time.time())}.mp3"
        dummy_output_path = Path(self.output_folder) / dummy_output_filename

        # Create a silent file as a placeholder
        silent_segment = AudioSegment.silent(
            duration=int(mix_plan["target_duration"] * 1000)
        )
        silent_segment.export(str(dummy_output_path), format="mp3")

        logger.warning(
            "Intelligent mix generation is currently a placeholder. Uses basic layering."
        )
        return dummy_output_path


# Example of how it might be used (for testing or integration)
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # Create dummy audio files for testing
    Path("input_clips_test").mkdir(exist_ok=True)
    for i in range(5):
        fname = Path(f"input_clips_test/sample_{i}.wav")
        if not fname.exists():  # Avoid recreating if they exist
            AudioSegment.silent(duration=10000).export(fname, format="wav")

    intelligent_mixer = IntelligentMixCreator(output_folder="output_mixes_intelligent")

    test_clip_paths = [Path(f"input_clips_test/sample_{i}.wav") for i in range(5)]
    for p in test_clip_paths:
        if not p.exists():
            logger.error(f"Test clip {p} does not exist. Skipping.")
            continue
        intelligent_mixer.add_clip_with_analysis(p)  # Analyze and cache

    # Create a sleep mix
    output_mix_path = intelligent_mixer.create_intelligent_mix(
        clip_paths=test_clip_paths,
        mix_type="sleep",
        target_duration_minutes=1,  # Short mix for testing
        sleep_phase="falling_asleep",
        add_binaural_beats=True,
        binaural_beat_freq=7.0,  # Theta wave for relaxation
    )

    if output_mix_path:
        logger.info(f"Test intelligent mix created at: {output_mix_path}")
    else:
        logger.error("Failed to create test intelligent mix.")
