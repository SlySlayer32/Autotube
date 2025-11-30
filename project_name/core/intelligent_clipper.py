"""
Intelligent Audio Clipping and Segmentation System

This module provides advanced audio analysis and segmentation capabilities
for extracting useful content from longer audio files.
"""

import logging
import json
import numpy as np
import librosa
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import soundfile as sf

from project_name.core.audio_similarity import AudioSimilarityMatcher

logger = logging.getLogger(__name__)


class IntelligentAudioClipper:
    """Advanced audio clipping and segmentation system."""
    
    def __init__(self):
        self.similarity_matcher = AudioSimilarityMatcher()
        self.sample_rate = 44100
        
    def analyze_and_extract_segments(self, audio_file_path: str, 
                                   output_dir: Optional[str] = None) -> Dict:
        """
        Analyze audio file and extract useful segments for library use.
        
        Args:
            audio_file_path: Path to the audio file to analyze
            output_dir: Directory to save extracted segments
            
        Returns:
            Dictionary containing analysis results and extracted segments
        """
        logger.info(f"Analyzing audio file: {audio_file_path}")
        
        # Load audio
        audio, sr = librosa.load(audio_file_path, sr=self.sample_rate)
        duration = len(audio) / sr
        
        # Comprehensive analysis
        analysis_results = {
            'file_info': {
                'path': audio_file_path,
                'duration': duration,
                'sample_rate': sr
            },
            'audio_characteristics': self._analyze_audio_characteristics(audio, sr),
            'segment_analysis': self._segment_audio(audio, sr),
            'loop_analysis': self._find_perfect_loops(audio, sr),
            'transition_points': self._find_transition_points(audio, sr),
            'quality_metrics': self._assess_audio_quality(audio, sr)
        }
        
        # Extract segments if output directory provided
        if output_dir:
            extracted_files = self._extract_segments_to_files(
                audio, sr, analysis_results, output_dir, audio_file_path
            )
            analysis_results['extracted_files'] = extracted_files
            
        return analysis_results
    
    def _analyze_audio_characteristics(self, audio: np.ndarray, sr: int) -> Dict:
        """Analyze fundamental audio characteristics."""
        try:
            # Basic audio properties
            rms = librosa.feature.rms(y=audio)[0]
            spectral_centroid = librosa.feature.spectral_centroid(y=audio, sr=sr)[0]
            spectral_rolloff = librosa.feature.spectral_rolloff(y=audio, sr=sr)[0]
            zero_crossing_rate = librosa.feature.zero_crossing_rate(audio)[0]
            
            # Tempo and rhythm
            tempo, beats = librosa.beat.beat_track(y=audio, sr=sr)
            
            # Frequency analysis
            stft = librosa.stft(audio)
            magnitude = np.abs(stft)
            
            # Classify content type
            content_type = self._classify_audio_content(audio, sr)
            
            return {
                'content_type': content_type,
                'energy_profile': {
                    'mean_rms': float(np.mean(rms)),
                    'rms_variation': float(np.std(rms)),
                    'dynamic_range': float(np.max(rms) - np.min(rms))
                },
                'spectral_profile': {
                    'mean_centroid': float(np.mean(spectral_centroid)),
                    'centroid_variation': float(np.std(spectral_centroid)),
                    'mean_rolloff': float(np.mean(spectral_rolloff)),
                    'brightness': float(np.mean(spectral_centroid) / (sr/2))
                },
                'temporal_profile': {
                    'tempo': float(tempo),
                    'rhythm_strength': float(np.std(np.diff(beats))),
                    'zero_crossing_rate': float(np.mean(zero_crossing_rate))
                },
                'frequency_distribution': self._analyze_frequency_bands(magnitude, sr)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing audio characteristics: {e}")
            return {}
    
    def _classify_audio_content(self, audio: np.ndarray, sr: int) -> str:
        """Classify the type of audio content."""
        try:
            # Simple heuristic-based classification
            rms = np.sqrt(np.mean(audio**2))
            zcr = np.mean(librosa.feature.zero_crossing_rate(audio))
            spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=audio, sr=sr))
            
            # Rain characteristics: high ZCR, broad spectrum, consistent energy
            if zcr > 0.1 and spectral_centroid > 2000:
                if rms > 0.1:
                    return "rain_heavy"
                else:
                    return "rain_light"
            
            # Thunder: sudden energy peaks, low frequency content
            if np.max(audio) > 0.7 and spectral_centroid < 1000:
                return "thunder"
            
            # Ambient/drone: steady energy, low variation
            if np.std(librosa.feature.rms(y=audio)) < 0.05:
                if spectral_centroid < 500:
                    return "ambient_drone"
                else:
                    return "ambient_texture"
            
            # Wind: moderate ZCR, energy variation
            if 0.05 < zcr < 0.15 and np.std(librosa.feature.rms(y=audio)) > 0.02:
                return "wind"
            
            return "unknown"
            
        except Exception as e:
            logger.error(f"Error classifying audio content: {e}")
            return "unknown"
    
    def _analyze_frequency_bands(self, magnitude: np.ndarray, sr: int) -> Dict:
        """Analyze energy distribution across frequency bands."""
        try:
            # Define frequency bands
            freqs = librosa.fft_frequencies(sr=sr)
            
            # Energy in different bands
            sub_bass = np.mean(magnitude[(freqs >= 20) & (freqs < 60)])
            bass = np.mean(magnitude[(freqs >= 60) & (freqs < 250)])
            low_mid = np.mean(magnitude[(freqs >= 250) & (freqs < 500)])
            mid = np.mean(magnitude[(freqs >= 500) & (freqs < 2000)])
            high_mid = np.mean(magnitude[(freqs >= 2000) & (freqs < 4000)])
            presence = np.mean(magnitude[(freqs >= 4000) & (freqs < 6000)])
            brilliance = np.mean(magnitude[(freqs >= 6000) & (freqs < 20000)])
            
            total_energy = sub_bass + bass + low_mid + mid + high_mid + presence + brilliance
            
            return {
                'sub_bass': float(sub_bass / total_energy),
                'bass': float(bass / total_energy),
                'low_mid': float(low_mid / total_energy),
                'mid': float(mid / total_energy),
                'high_mid': float(high_mid / total_energy),
                'presence': float(presence / total_energy),
                'brilliance': float(brilliance / total_energy)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing frequency bands: {e}")
            return {}
    
    def _segment_audio(self, audio: np.ndarray, sr: int) -> List[Dict]:
        """Segment audio into distinct sections."""
        try:
            # Use onset detection for segmentation
            onset_frames = librosa.onset.onset_detect(y=audio, sr=sr, units='frames')
            onset_times = librosa.frames_to_time(onset_frames, sr=sr)
            
            # Also use spectral change points
            chroma = librosa.feature.chroma_stft(y=audio, sr=sr)
            tempo, beats = librosa.beat.beat_track(y=audio, sr=sr)
            
            # Simple segmentation based on significant changes
            segments = []
            segment_length = 30  # 30 second segments
            
            for i in range(0, len(audio), sr * segment_length):
                end_idx = min(i + sr * segment_length, len(audio))
                segment_audio = audio[i:end_idx]
                
                if len(segment_audio) < sr * 5:  # Skip segments shorter than 5 seconds
                    continue
                
                segment_analysis = {
                    'start_time': i / sr,
                    'end_time': end_idx / sr,
                    'duration': len(segment_audio) / sr,
                    'energy': float(np.sqrt(np.mean(segment_audio**2))),
                    'spectral_centroid': float(np.mean(
                        librosa.feature.spectral_centroid(y=segment_audio, sr=sr)
                    )),
                    'loop_potential': self._assess_loop_potential(segment_audio, sr),
                    'transition_suitability': self._assess_transition_suitability(segment_audio, sr)
                }
                
                segments.append(segment_analysis)
            
            return segments
            
        except Exception as e:
            logger.error(f"Error segmenting audio: {e}")
            return []
    
    def _find_perfect_loops(self, audio: np.ndarray, sr: int) -> List[Dict]:
        """Find segments that can loop seamlessly."""
        try:
            loops = []
            
            # Test different loop lengths
            loop_lengths = [10, 15, 20, 30, 45, 60]  # seconds
            
            for length in loop_lengths:
                length_samples = int(length * sr)
                
                if length_samples > len(audio):
                    continue
                
                # Test multiple starting points
                step = sr * 5  # Every 5 seconds
                
                for start_idx in range(0, len(audio) - length_samples, step):
                    end_idx = start_idx + length_samples
                    
                    # Extract potential loop
                    loop_segment = audio[start_idx:end_idx]
                    
                    # Test loop quality
                    loop_quality = self._assess_loop_quality(loop_segment, sr)
                    
                    if loop_quality['seamless_score'] > 0.7:  # Good loop threshold
                        loops.append({
                            'start_time': start_idx / sr,
                            'end_time': end_idx / sr,
                            'duration': length,
                            'quality_metrics': loop_quality,
                            'loop_type': self._classify_loop_type(loop_segment, sr)
                        })
            
            # Sort by quality and return best candidates
            loops.sort(key=lambda x: x['quality_metrics']['seamless_score'], reverse=True)
            return loops[:10]  # Top 10 loop candidates
            
        except Exception as e:
            logger.error(f"Error finding perfect loops: {e}")
            return []
    
    def _assess_loop_quality(self, audio: np.ndarray, sr: int) -> Dict:
        """Assess how well an audio segment can loop."""
        try:
            # Compare beginning and end for seamless transition
            fade_length = int(0.5 * sr)  # 0.5 second comparison
            
            if len(audio) < fade_length * 2:
                return {'seamless_score': 0.0}
            
            beginning = audio[:fade_length]
            ending = audio[-fade_length:]
            
            # Correlation between beginning and end
            correlation = np.corrcoef(beginning, ending)[0, 1]
            if np.isnan(correlation):
                correlation = 0.0
            
            # RMS energy difference
            rms_beginning = np.sqrt(np.mean(beginning**2))
            rms_ending = np.sqrt(np.mean(ending**2))
            energy_match = 1.0 - abs(rms_beginning - rms_ending)
            
            # Spectral similarity
            spec_beginning = np.abs(librosa.stft(beginning))
            spec_ending = np.abs(librosa.stft(ending))
            
            spec_corr = np.corrcoef(
                np.mean(spec_beginning, axis=1),
                np.mean(spec_ending, axis=1)
            )[0, 1]
            
            if np.isnan(spec_corr):
                spec_corr = 0.0
            
            # Overall seamless score
            seamless_score = (correlation * 0.4 + energy_match * 0.3 + spec_corr * 0.3)
            
            return {
                'seamless_score': float(max(0, seamless_score)),
                'correlation': float(correlation),
                'energy_match': float(energy_match),
                'spectral_match': float(spec_corr)
            }
            
        except Exception as e:
            logger.error(f"Error assessing loop quality: {e}")
            return {'seamless_score': 0.0}
    
    def _classify_loop_type(self, audio: np.ndarray, sr: int) -> str:
        """Classify the type of loop based on its characteristics."""
        try:
            # Analyze the loop characteristics
            rms = np.mean(librosa.feature.rms(y=audio))
            zcr = np.mean(librosa.feature.zero_crossing_rate(audio))
            spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=audio, sr=sr))
            
            # Simple classification
            if rms < 0.01:
                return "ambient_quiet"
            elif zcr > 0.1:
                return "textural_busy"
            elif spectral_centroid > 3000:
                return "bright_atmospheric"
            elif spectral_centroid < 500:
                return "bass_drone"
            else:
                return "balanced_ambient"
                
        except Exception as e:
            logger.error(f"Error classifying loop type: {e}")
            return "unknown"
    
    def _find_transition_points(self, audio: np.ndarray, sr: int) -> List[Dict]:
        """Find good points for transitioning between different audio content."""
        try:
            # Find points with low energy (good for transitions)
            rms = librosa.feature.rms(y=audio, hop_length=sr//4)[0]  # Every 0.25 seconds
            
            # Find local minima in energy
            from scipy.signal import argrelmin
            
            min_indices = argrelmin(rms, order=int(sr/2))[0]  # At least 0.5 seconds apart
            
            transitions = []
            for idx in min_indices:
                time = idx * 0.25  # Convert to time
                
                # Get surrounding context for analysis
                start_sample = max(0, int((time - 1) * sr))
                end_sample = min(len(audio), int((time + 1) * sr))
                context = audio[start_sample:end_sample]
                
                transition_quality = self._assess_transition_quality(context, sr)
                
                transitions.append({
                    'time': time,
                    'energy_level': float(rms[idx]),
                    'quality_score': transition_quality
                })
            
            # Sort by quality and return best candidates
            transitions.sort(key=lambda x: x['quality_score'], reverse=True)
            return transitions[:20]  # Top 20 transition points
            
        except Exception as e:
            logger.error(f"Error finding transition points: {e}")
            return []
    
    def _assess_transition_quality(self, audio: np.ndarray, sr: int) -> float:
        """Assess how suitable a point is for transitions."""
        try:
            # Low energy is good for transitions
            energy = np.sqrt(np.mean(audio**2))
            energy_score = max(0, 1.0 - energy * 5)  # Invert energy
            
            # Stable spectral content is good
            spectral_centroid = librosa.feature.spectral_centroid(y=audio, sr=sr)[0]
            spectral_stability = 1.0 - min(1.0, np.std(spectral_centroid) / 1000)
            
            return float(energy_score * 0.6 + spectral_stability * 0.4)
            
        except Exception as e:
            logger.error(f"Error assessing transition quality: {e}")
            return 0.0
    
    def _assess_audio_quality(self, audio: np.ndarray, sr: int) -> Dict:
        """Assess overall audio quality metrics."""
        try:
            # Dynamic range
            dynamic_range = 20 * np.log10(np.max(np.abs(audio))) - 20 * np.log10(np.sqrt(np.mean(audio**2)))
            
            # Clipping detection
            clipping_ratio = np.sum(np.abs(audio) > 0.99) / len(audio)
            
            # Signal-to-noise ratio estimation
            # Simple approach: compare energy in different frequency bands
            stft = librosa.stft(audio)
            magnitude = np.abs(stft)
            
            # Estimate noise floor (lowest 10% of magnitudes)
            noise_floor = np.percentile(magnitude, 10)
            signal_level = np.percentile(magnitude, 90)
            snr_estimate = 20 * np.log10(signal_level / max(noise_floor, 1e-10))
            
            return {
                'dynamic_range_db': float(dynamic_range),
                'clipping_ratio': float(clipping_ratio),
                'estimated_snr_db': float(snr_estimate),
                'overall_quality': self._calculate_overall_quality(dynamic_range, clipping_ratio, snr_estimate)
            }
            
        except Exception as e:
            logger.error(f"Error assessing audio quality: {e}")
            return {}
    
    def _calculate_overall_quality(self, dynamic_range: float, clipping_ratio: float, snr: float) -> float:
        """Calculate overall quality score from individual metrics."""
        # Quality scoring (0-1 scale)
        dr_score = min(1.0, max(0.0, dynamic_range / 40))  # Good dynamic range > 40dB
        clipping_score = max(0.0, 1.0 - clipping_ratio * 100)  # Penalize clipping heavily
        snr_score = min(1.0, max(0.0, snr / 60))  # Good SNR > 60dB
        
        return float(dr_score * 0.4 + clipping_score * 0.4 + snr_score * 0.2)
    
    def _assess_loop_potential(self, audio: np.ndarray, sr: int) -> float:
        """Quick assessment of how well this segment might loop."""
        if len(audio) < sr * 5:  # Need at least 5 seconds
            return 0.0
            
        return self._assess_loop_quality(audio, sr)['seamless_score']
    
    def _assess_transition_suitability(self, audio: np.ndarray, sr: int) -> float:
        """Quick assessment of transition suitability."""
        # Look for stable, low-energy sections
        rms = np.sqrt(np.mean(audio**2))
        rms_variation = np.std(librosa.feature.rms(y=audio)[0])
        
        # Good for transitions: low energy, low variation
        energy_score = max(0, 1.0 - rms * 3)
        stability_score = max(0, 1.0 - rms_variation * 10)
        
        return float(energy_score * 0.6 + stability_score * 0.4)
    
    def _extract_segments_to_files(self, audio: np.ndarray, sr: int, 
                                 analysis: Dict, output_dir: str, 
                                 source_file: str) -> List[str]:
        """Extract the best segments to individual files."""
        try:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            source_name = Path(source_file).stem
            extracted_files = []
            
            # Extract best loops
            loops = analysis.get('loop_analysis', [])
            for i, loop in enumerate(loops[:5]):  # Top 5 loops
                start_sample = int(loop['start_time'] * sr)
                end_sample = int(loop['end_time'] * sr)
                loop_audio = audio[start_sample:end_sample]
                
                filename = f"{source_name}_loop_{i+1}_{loop['duration']}s.wav"
                file_path = output_path / filename
                
                # Add crossfade for perfect looping
                loop_audio = self._add_loop_crossfade(loop_audio, sr)
                
                sf.write(str(file_path), loop_audio, sr)
                extracted_files.append(str(file_path))
                
                # Save loop metadata
                metadata = {
                    'source_file': source_file,
                    'segment_type': 'loop',
                    'start_time': loop['start_time'],
                    'end_time': loop['end_time'],
                    'quality_metrics': loop['quality_metrics'],
                    'loop_type': loop['loop_type']
                }
                
                metadata_path = file_path.with_suffix('.json')
                with open(metadata_path, 'w') as f:
                    json.dump(metadata, f, indent=2)
            
            # Extract best segments for other uses
            segments = analysis.get('segment_analysis', [])
            high_quality_segments = [s for s in segments if s.get('energy', 0) > 0.01]
            
            for i, segment in enumerate(high_quality_segments[:10]):  # Top 10 segments
                start_sample = int(segment['start_time'] * sr)
                end_sample = int(segment['end_time'] * sr)
                segment_audio = audio[start_sample:end_sample]
                
                filename = f"{source_name}_segment_{i+1}_{segment['duration']:.1f}s.wav"
                file_path = output_path / filename
                
                sf.write(str(file_path), segment_audio, sr)
                extracted_files.append(str(file_path))
            
            logger.info(f"Extracted {len(extracted_files)} segments from {source_file}")
            return extracted_files
            
        except Exception as e:
            logger.error(f"Error extracting segments: {e}")
            return []
    
    def _add_loop_crossfade(self, audio: np.ndarray, sr: int, fade_duration: float = 0.1) -> np.ndarray:
        """Add crossfade to audio for perfect looping."""
        try:
            fade_samples = int(fade_duration * sr)
            
            if len(audio) < fade_samples * 2:
                return audio
            
            # Create crossfade
            fade_out = np.linspace(1, 0, fade_samples)
            fade_in = np.linspace(0, 1, fade_samples)
            
            # Apply crossfade
            audio[-fade_samples:] = audio[-fade_samples:] * fade_out + audio[:fade_samples] * fade_in
            
            return audio
            
        except Exception as e:
            logger.error(f"Error adding loop crossfade: {e}")
            return audio


# Example usage and testing
if __name__ == "__main__":
    clipper = IntelligentAudioClipper()
    
    # Example: analyze a rain recording
    # results = clipper.analyze_and_extract_segments(
    #     "path/to/long_rain_recording.wav",
    #     "extracted_segments/"
    # )
    
    # print(json.dumps(results, indent=2))
