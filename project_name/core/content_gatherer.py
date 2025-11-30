"""
Advanced Content Gathering System

This module provides intelligent content acquisition for building
a comprehensive audio library for seamless mix creation.
"""

import logging
import os
import json
from pathlib import Path
from typing import Dict, List, Optional
import requests
import librosa
import numpy as np
import shutil

from project_name.api.freesound_api import FreesoundAPI
from project_name.core.audio_similarity import AudioSimilarityMatcher

logger = logging.getLogger(__name__)


class ContentGatherer:
    """Advanced content gathering and organization system."""
    
    def __init__(self, freesound_api_key: Optional[str] = None):
        self.freesound_api = FreesoundAPI(freesound_api_key) if freesound_api_key else None
        self.similarity_matcher = AudioSimilarityMatcher()
        self.library_path = Path("audio_library")
        self.library_path.mkdir(exist_ok=True)
          # Content categories and their search parameters
        self.content_categories = {
            'rain': {
                'light': {
                    'queries': ['+rain +gentle +soft -thunder -storm', '"light rain" +peaceful', '+drizzle +calm'],
                    'duration_range': (30, 300),
                    'category': 'Sound effects',
                    'subcategory': 'Natural elements',
                    'descriptors': 'ac_brightness:[0 TO 25] ac_roughness:[0 TO 20]'
                },
                'medium': {
                    'queries': ['+rain +steady -storm -thunder', '"rain loop" +ambient', '+rainfall +calm'],
                    'duration_range': (30, 600),
                    'category': 'Soundscapes',
                    'subcategory': 'Nature',
                    'descriptors': 'ac_brightness:[0 TO 30] ac_warmth:[60 TO 100]'
                },
                'heavy': {
                    'queries': ['+rain +heavy -thunder -storm', '+downpour +rain -wind', '+rain +intense -thunder'],
                    'duration_range': (20, 300),
                    'category': 'Sound effects',
                    'subcategory': 'Natural elements',
                    'descriptors': 'ac_brightness:[10 TO 40] ac_hardness:[20 TO 50]'
                },
                'on_roof': {
                    'queries': ['+rain +roof -thunder', '+rain +metal -storm', '+rain +tin -wind'],
                    'duration_range': (30, 300),
                    'category': 'Sound effects',
                    'subcategory': 'Natural elements'
                },
                'on_leaves': {
                    'queries': ['+rain +forest -thunder', '+rain +leaves -storm', '+rain +trees -wind'],
                    'duration_range': (30, 300),
                    'category': 'Soundscapes',
                    'subcategory': 'Nature'
                }
            },
            'thunder': {
                'distant': {
                    'queries': ['+thunder +distant', '+thunder +far', '+thunder +soft'],
                    'duration_range': (5, 30),
                    'category': 'Sound effects',
                    'subcategory': 'Natural elements'
                },
                'close': {
                    'queries': ['+thunder +crack', '+thunder +clap', '+thunder +close'],
                    'duration_range': (2, 15),
                    'category': 'Sound effects',
                    'subcategory': 'Natural elements'
                },
                'rumble': {
                    'queries': ['+thunder +rumble', '+thunder +rolling', '+thunder +low'],
                    'duration_range': (10, 60),
                    'category': 'Sound effects',
                    'subcategory': 'Natural elements'
                }
            },
            'ambient': {
                'forest': {
                    'queries': ['+forest +ambience +calm', '+woodland +peaceful', '+forest +atmosphere -birds'],
                    'duration_range': (60, 1800),
                    'category': 'Soundscapes',
                    'subcategory': 'Nature',
                    'descriptors': 'ac_warmth:[70 TO 100] ac_brightness:[0 TO 20] ac_single_event:false'
                },
                'ocean': {
                    'queries': ['+ocean +waves +calm', '+sea +ambience -storm', '+beach +waves +peaceful'],
                    'duration_range': (60, 1800),
                    'category': 'Soundscapes',
                    'subcategory': 'Nature',
                    'descriptors': 'ac_warmth:[60 TO 100] ac_hardness:[0 TO 25] ac_single_event:false'
                },
                'wind': {
                    'queries': ['+wind +gentle +ambience', '+breeze +soft', '+wind +trees +calm'],
                    'duration_range': (30, 600),
                    'category': 'Sound effects',
                    'subcategory': 'Natural elements',
                    'descriptors': 'ac_brightness:[0 TO 30] ac_roughness:[0 TO 30]'
                },
                'night': {
                    'queries': ['+night +ambience +calm', '+crickets +peaceful', '+night +forest +quiet'],
                    'duration_range': (60, 1800),
                    'category': 'Soundscapes',
                    'subcategory': 'Nature',
                    'descriptors': 'ac_brightness:[0 TO 15] ac_warmth:[50 TO 100]'
                }
            },
            'binaural_sources': {
                'sine_tones': {
                    'queries': ['+sine +wave +pure', '+tone +clean', '+sine +simple'],
                    'duration_range': (60, 3600),
                    'descriptors': 'ac_single_event:false ac_roughness:[0 TO 5]'
                },
                'drones': {
                    'queries': ['+ambient +drone +meditation', '+sustained +tone +calm', '+drone +peaceful'],
                    'duration_range': (120, 3600),
                    'descriptors': 'ac_single_event:false ac_roughness:[0 TO 15] ac_brightness:[0 TO 20]'
                }
            }
        }
    
    def gather_all_content(self, max_per_category: int = 50):
        """
        Gather content for all categories systematically.
        
        Args:
            max_per_category: Maximum files to download per subcategory
        """
        if not self.freesound_api:
            logger.error("Freesound API key required for content gathering")
            return
            
        logger.info("Starting comprehensive content gathering...")
        
        for main_category, subcategories in self.content_categories.items():
            category_path = self.library_path / main_category
            category_path.mkdir(exist_ok=True)
            
            for sub_category, config in subcategories.items():
                sub_path = category_path / sub_category
                sub_path.mkdir(exist_ok=True)
                
                logger.info(f"Gathering {main_category}/{sub_category}...")
                self._gather_category_content(config, sub_path, max_per_category)

    def _gather_category_content(self, config: Dict, output_path: Path, max_files: int):
        """Gather content for a specific category using enhanced search strategies."""
        downloaded_count = 0
        
        for query in config['queries']:
            if downloaded_count >= max_files:
                break
                
            try:
                # Enhanced search with advanced filtering
                search_params = {
                    'query': query,
                    'page_size': min(50, max_files - downloaded_count),
                    'sort': "rating_desc",  # Get highest rated first
                    'rating_min': 3.0,  # Minimum 3-star rating
                    'downloads_min': 5,  # At least 5 downloads for quality assurance
                    'duration_range': config['duration_range'],
                    'license_filter': "Attribution"  # Prefer Attribution license
                }
                
                # Add category-specific filters
                if 'category' in config:
                    search_params['category'] = config['category']
                if 'subcategory' in config:
                    search_params['subcategory'] = config['subcategory']
                if 'descriptors' in config:
                    search_params['descriptors_filter'] = config['descriptors']
                
                # Add therapeutic-focused tags
                therapeutic_tags = ['ambient', 'calm', 'peaceful', 'relaxation']
                exclude_tags = ['loud', 'harsh', 'sudden', 'alarm', 'aggressive']
                search_params['filter_tags'] = therapeutic_tags + [f'-{tag}' for tag in exclude_tags]
                
                results = self.freesound_api.search(**search_params)
                
                if 'results' not in results:
                    logger.warning(f"No results for query: {query}")
                    continue
                    
                for sound in results['results']:
                    if downloaded_count >= max_files:
                        break
                        
                    # Enhanced quality filtering
                    if self._meets_enhanced_quality_criteria(sound, config):
                        success = self._download_and_process_sound(sound, output_path)
                        if success:
                            downloaded_count += 1
                            logger.info(f"Successfully downloaded {sound['name']} ({downloaded_count}/{max_files})")
                            
            except Exception as e:
                logger.error(f"Error gathering content for query '{query}': {e}")
                continue
                
        logger.info(f"Completed category collection: {downloaded_count}/{max_files} files downloaded")

    def _meets_enhanced_quality_criteria(self, sound: Dict, config: Dict) -> bool:
        """Enhanced quality criteria checking using metadata and AudioCommons data."""
        # Basic duration check
        duration = sound.get('duration', 0)
        min_dur, max_dur = config['duration_range']
        
        if not (min_dur <= duration <= max_dur):
            logger.debug(f"Skipping {sound['name']}: duration {duration}s not in range [{min_dur}, {max_dur}]")
            return False
            
        # License check (prefer open licenses)
        license_name = sound.get('license', '').lower()
        preferred_licenses = ['creative commons 0', 'attribution', 'cc0', 'cc-by']
        if not any(lic in license_name for lic in preferred_licenses):
            logger.debug(f"Skipping {sound['name']}: license '{license_name}' not preferred")
            return False
            
        # Rating and popularity check
        avg_rating = sound.get('avg_rating', 0)
        num_ratings = sound.get('num_ratings', 0)
        num_downloads = sound.get('num_downloads', 0)
        
        if num_ratings > 0 and avg_rating < 3.0:
            logger.debug(f"Skipping {sound['name']}: low rating {avg_rating}")
            return False
            
        if num_downloads < 5:  # Require some validation from community
            logger.debug(f"Skipping {sound['name']}: too few downloads ({num_downloads})")
            return False
            
        # Tag-based filtering for therapeutic quality
        tags = [tag.lower() for tag in sound.get('tags', [])]
        
        # Negative tags that indicate poor therapeutic value
        negative_tags = [
            'loud', 'aggressive', 'harsh', 'sudden', 'alarm', 'shock', 'scary', 
            'horror', 'screaming', 'noise', 'distorted', 'glitch', 'industrial',
            'metal', 'rock', 'techno', 'beat', 'drum', 'bass', 'synth'
        ]
        
        if any(neg_tag in ' '.join(tags) for neg_tag in negative_tags):
            logger.debug(f"Skipping {sound['name']}: contains negative tags in {tags}")
            return False
            
        # Positive tags that indicate good therapeutic value
        positive_tags = [
            'ambient', 'calm', 'peaceful', 'relaxing', 'meditation', 'sleep',
            'nature', 'gentle', 'soft', 'quiet', 'soothing', 'tranquil'
        ]
        
        # Require at least one positive therapeutic tag OR be in nature/ambient category
        has_positive_tag = any(pos_tag in ' '.join(tags) for pos_tag in positive_tags)
        is_nature_category = any(term in ' '.join(tags) for term in ['nature', 'forest', 'ocean', 'rain', 'wind', 'water'])
        
        if not (has_positive_tag or is_nature_category):
            logger.debug(f"Skipping {sound['name']}: lacks therapeutic tags in {tags}")
            return False
            
        # AudioCommons analysis check (if available)
        ac_analysis = sound.get('ac_analysis', {})
        if ac_analysis:
            # Check for therapeutic audio characteristics
            brightness = ac_analysis.get('ac_brightness', 50)  # Lower = darker, calmer
            hardness = ac_analysis.get('ac_hardness', 50)     # Lower = softer
            roughness = ac_analysis.get('ac_roughness', 50)   # Lower = smoother
            
            # Therapeutic sounds should generally be darker, softer, smoother
            if brightness > 70:  # Too bright/harsh
                logger.debug(f"Skipping {sound['name']}: too bright (ac_brightness: {brightness})")
                return False
                
            if hardness > 60:  # Too hard/aggressive
                logger.debug(f"Skipping {sound['name']}: too hard (ac_hardness: {hardness})")
                return False
                
            if roughness > 50:  # Too rough/textured
                logger.debug(f"Skipping {sound['name']}: too rough (ac_roughness: {roughness})")
                return False
                
        return True
    
    def _download_and_process_sound(self, sound: Dict, output_path: Path) -> bool:
        """Download and process a sound file."""
        try:
            sound_id = sound['id']
            filename = f"{sound_id}_{sound['name'][:50]}.wav"
            filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_', '.')).rstrip()
            file_path = output_path / filename
            
            # Skip if already exists
            if file_path.exists():
                return True
                
            # Download preview (high quality preview if available)
            preview_url = None
            if 'previews' in sound:
                # Prefer high quality preview
                if 'preview-hq-mp3' in sound['previews']:
                    preview_url = sound['previews']['preview-hq-mp3']
                elif 'preview-lq-mp3' in sound['previews']:
                    preview_url = sound['previews']['preview-lq-mp3']
                    
            if not preview_url:
                return False
                
            # Download file
            response = requests.get(preview_url, timeout=30)
            response.raise_for_status()
            
            # Save and convert to WAV if needed
            temp_file = file_path.with_suffix('.mp3')
            with open(temp_file, 'wb') as f:
                f.write(response.content)
                
            # Convert to WAV and analyze
            try:
                audio, sr = librosa.load(str(temp_file), sr=44100)
                
                # Basic quality checks
                if len(audio) < sr * 5:  # At least 5 seconds
                    temp_file.unlink()
                    return False
                    
                # Save as WAV
                import soundfile as sf
                sf.write(str(file_path), audio, sr)
                temp_file.unlink()
                  # Save metadata
                metadata = {
                    'freesound_id': sound_id,
                    'name': sound['name'],
                    'description': sound.get('description', ''),
                    'tags': sound.get('tags', []),
                    'duration': sound.get('duration', 0),
                    'license': sound.get('license', ''),
                    'username': sound.get('username', ''),
                    'download_date': None,  # Would add timestamp
                    'local_analysis': {}
                }
                
                metadata_path = file_path.with_suffix('.json')
                with open(metadata_path, 'w') as f:
                    json.dump(metadata, f, indent=2)
                    
                logger.info(f"Downloaded and processed: {filename}")
                return True
                
            except Exception as e:
                logger.error(f"Error processing audio file {filename}: {e}")
                if temp_file.exists():
                    temp_file.unlink()
                if file_path.exists():
                    file_path.unlink()
                return False
                
        except Exception as e:
            logger.error(f"Error downloading sound {sound['id']}: {e}")
            return False
    
    def generate_synthetic_binaural_library(self, short_duration: bool = True):
        """
        Generate a space-efficient synthetic binaural beat library.
        
        Args:
            short_duration: If True, create short (60s) loops. If False, create long (1hr) tracks.
        """
        logger.info("Generating space-efficient synthetic binaural beat library...")
        
        binaural_path = self.library_path / "binaural_beats"
        binaural_path.mkdir(exist_ok=True)
        
        # Binaural beat frequencies for different states
        beat_frequencies = {
            'delta_sleep': [0.5, 1.0, 2.0, 3.0, 4.0],  # Reduced set
            'theta_rem': [4.0, 5.0, 6.0, 7.0, 8.0],
            'alpha_relax': [8.0, 9.0, 10.0, 11.0, 12.0],
            'beta_focus': [13.0, 16.0, 20.0, 25.0, 30.0]
        }
        
        base_frequencies = [440]  # Single base frequency to save space
        duration = 60 if short_duration else 3600  # 1 minute vs 1 hour
        
        logger.info(f"Creating {duration}s duration tracks (~{duration/60:.1f} min each)")
        
        for state, beat_freqs in beat_frequencies.items():
            state_path = binaural_path / state
            state_path.mkdir(exist_ok=True)
            
            for base_freq in base_frequencies:
                for beat_freq in beat_freqs:
                    self._generate_binaural_beat(
                        base_freq, beat_freq, state_path, duration=duration
                    )
    
    def _generate_binaural_beat(self, base_freq: float, beat_freq: float, 
                              output_path: Path, duration: int = 3600):
        """Generate a single binaural beat track."""
        try:
            filename = f"binaural_{base_freq}Hz_beat_{beat_freq}Hz.wav"
            file_path = output_path / filename
            
            if file_path.exists():
                return
                
            sample_rate = 44100
            t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
            
            # Generate left and right channels
            left_freq = base_freq
            right_freq = base_freq + beat_freq
            
            left_channel = 0.3 * np.sin(2 * np.pi * left_freq * t)
            right_channel = 0.3 * np.sin(2 * np.pi * right_freq * t)
            
            # Apply fade in/out
            fade_samples = int(sample_rate * 10)  # 10 second fade
            fade_in = np.linspace(0, 1, fade_samples)
            fade_out = np.linspace(1, 0, fade_samples)
            
            left_channel[:fade_samples] *= fade_in
            left_channel[-fade_samples:] *= fade_out
            right_channel[:fade_samples] *= fade_in
            right_channel[-fade_samples:] *= fade_out
            
            # Combine channels
            stereo_audio = np.column_stack((left_channel, right_channel))
            
            # Save
            import soundfile as sf
            sf.write(str(file_path), stereo_audio, sample_rate)
            
            # Save metadata
            metadata = {
                'type': 'binaural_beat',
                'base_frequency': base_freq,
                'beat_frequency': beat_freq,
                'duration': duration,
                'sample_rate': sample_rate,
                'purpose': self._get_binaural_purpose(beat_freq)
            }
            
            metadata_path = file_path.with_suffix('.json')
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
                
            logger.info(f"Generated binaural beat: {filename}")
            
        except Exception as e:
            logger.error(f"Error generating binaural beat {base_freq}Hz/{beat_freq}Hz: {e}")
    
    def _get_binaural_purpose(self, beat_freq: float) -> str:
        """Get the purpose/effect of a binaural beat frequency."""
        if beat_freq <= 4:
            return "deep_sleep"
        elif beat_freq <= 8:
            return "rem_sleep_creativity"
        elif beat_freq <= 12:
            return "relaxation_meditation"
        elif beat_freq <= 30:
            return "focus_concentration"
        else:
            return "high_alertness"
    
    def analyze_library_content(self):
        """Analyze all content in the library using OpenL3."""
        logger.info("Analyzing library content with OpenL3...")
        
        for audio_file in self.library_path.rglob("*.wav"):
            try:
                # Skip if analysis already exists
                analysis_file = audio_file.with_suffix('.analysis.json')
                if analysis_file.exists():
                    continue
                    
                # Extract OpenL3 embedding
                embedding = self.similarity_matcher.extract_embedding(str(audio_file))
                
                # Additional analysis
                audio, sr = librosa.load(str(audio_file), sr=44100)
                
                analysis = {
                    'openl3_embedding_shape': embedding.shape if embedding is not None else None,
                    'duration': len(audio) / sr,
                    'rms_energy': float(np.sqrt(np.mean(audio**2))),
                    'spectral_centroid': float(np.mean(librosa.feature.spectral_centroid(y=audio, sr=sr))),
                    'zero_crossing_rate': float(np.mean(librosa.feature.zero_crossing_rate(audio))),
                    'tempo': float(librosa.beat.tempo(y=audio, sr=sr)[0]),
                    'loop_candidates': self._find_loop_candidates(audio, sr)
                }
                
                with open(analysis_file, 'w') as f:
                    json.dump(analysis, f, indent=2)
                    
                logger.info(f"Analyzed: {audio_file.name}")
                
            except Exception as e:
                logger.error(f"Error analyzing {audio_file}: {e}")
    
    def _find_loop_candidates(self, audio: np.ndarray, sr: int) -> List[Dict]:
        """Find potential loop points in audio."""
        # Simple implementation - could be enhanced
        candidates = []
        
        # Look for segments that are similar to the beginning
        segment_length = min(len(audio), sr * 30)  # 30 second max
        start_segment = audio[:segment_length]
        
        # Check every 5 seconds for similar segments
        step = sr * 5
        for i in range(step, len(audio) - segment_length, step):
            test_segment = audio[i:i + segment_length]
            
            # Simple correlation check
            correlation = np.corrcoef(start_segment, test_segment)[0, 1]
            
            if correlation > 0.7:  # High similarity
                candidates.append({
                    'start_time': 0,
                    'end_time': i / sr,
                    'correlation': float(correlation)
                })
                
        return candidates[:5]  # Return top 5 candidates


if __name__ == "__main__":
    # Example usage
    gatherer = ContentGatherer()
    
    # Generate synthetic binaural library first (no API key needed)
    gatherer.generate_synthetic_binaural_library()
    
    # If you have Freesound API key, gather real content
    # gatherer.gather_all_content()
    
    # Analyze all content
    gatherer.analyze_library_content()
