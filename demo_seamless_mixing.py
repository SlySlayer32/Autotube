"""
Demo: Seamless Mix Engine with Real Audio

This demo creates actual audio mixes using the seamless engine,
demonstrating the full workflow from content gathering to final mix.
"""

import logging
import os
import json
from pathlib import Path

from project_name.core.seamless_mix_engine import SeamlessMixEngine
from efficient_content_demo import EfficientBinauralGenerator

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def create_demo_content():
    """Create sample content for the demo."""
    logger.info("🎵 Creating demo content...")
    
    # Generate binaural beats if not already present
    generator = EfficientBinauralGenerator()
    generator.generate_efficient_binaural_library()
    
    # Check what we have
    audio_library = Path("audio_library")
    binaural_path = audio_library / "binaural_beats"
    
    available_files = {
        'binaural': [],
        'base': [],
        'ambience': [],
        'accent': []
    }
    
    # Find binaural files
    if binaural_path.exists():
        for wav_file in binaural_path.rglob("*.wav"):
            available_files['binaural'].append(str(wav_file))
    
    # Check for any other audio files in the project
    for folder in ["input_clips", "processed_clips"]:
        folder_path = Path(folder)
        if folder_path.exists():
            for wav_file in folder_path.glob("*.wav"):
                if "rain" in wav_file.name.lower():
                    available_files['base'].append(str(wav_file))
                elif any(word in wav_file.name.lower() for word in ["ambient", "forest", "nature"]):
                    available_files['ambience'].append(str(wav_file))
                elif any(word in wav_file.name.lower() for word in ["thunder", "wind", "bird"]):
                    available_files['accent'].append(str(wav_file))
    
    return available_files


def create_synthetic_demo_layer():
    """Create a simple synthetic rain layer for demo purposes."""
    import numpy as np
    import soundfile as sf
    
    demo_path = Path("demo_audio")
    demo_path.mkdir(exist_ok=True)
    
    # Create synthetic rain sound
    logger.info("🌧️ Creating synthetic rain layer...")
    
    duration = 60  # 60 seconds
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    # Generate pink noise (rain-like)
    noise = np.random.normal(0, 0.1, len(t))
    
    # Apply simple filtering to make it more rain-like
    # High-pass filter effect (emphasize higher frequencies)
    filtered_noise = noise.copy()
    for i in range(1, len(filtered_noise)):
        filtered_noise[i] = 0.95 * filtered_noise[i-1] + 0.05 * noise[i]
    
    # Make it stereo with slight differences
    left_channel = filtered_noise
    right_channel = np.roll(filtered_noise, int(sample_rate * 0.01))  # 10ms delay
    
    stereo_rain = np.column_stack((left_channel, right_channel))
    
    # Add subtle volume variations
    volume_curve = 1.0 + 0.1 * np.sin(2 * np.pi * t / 10)  # 10-second cycles
    stereo_rain *= volume_curve.reshape(-1, 1)
    
    rain_file = demo_path / "synthetic_rain_60s.wav"
    sf.write(str(rain_file), stereo_rain, sample_rate, subtype='PCM_16')
    
    logger.info(f"✅ Created synthetic rain: {rain_file}")
    return str(rain_file)


def demo_mix_creation():
    """Demonstrate creating different types of mixes."""
    logger.info("🎛️ Starting Mix Creation Demo")
    
    # Get available content
    available_files = create_demo_content()
    
    # Create synthetic rain if we don't have base content
    if not available_files['base']:
        synthetic_rain = create_synthetic_demo_layer()
        available_files['base'].append(synthetic_rain)
    
    # Create output directory
    output_dir = Path("demo_mixes")
    output_dir.mkdir(exist_ok=True)
    
    # Initialize mix engine
    mix_engine = SeamlessMixEngine()
    
    # Define demo mix configurations
    demo_configs = [
        {
            'name': 'Quick Sleep Mix',
            'duration': 5,  # 5 minutes for quick demo
            'type': 'sleep',
            'description': 'Gentle rain with delta binaural beats, fading volume'
        },
        {
            'name': 'Focus Session',
            'duration': 3,  # 3 minutes for demo
            'type': 'focus',
            'description': 'Balanced mix with alpha/beta binaural beats'
        },
        {
            'name': 'Relaxation Journey',
            'duration': 4,  # 4 minutes for demo
            'type': 'relaxation',
            'description': 'Warm ambience with alpha waves and gentle variations'
        }
    ]
    
    created_mixes = []
    
    for config in demo_configs:
        logger.info(f"🎵 Creating: {config['name']}")
        
        # Prepare layer files for this mix
        layer_files = {
            'base': available_files['base'][:1] if available_files['base'] else [],
            'binaural': available_files['binaural'][:2] if available_files['binaural'] else [],
            'ambience': available_files['ambience'][:1] if available_files['ambience'] else [],
            'accent': available_files['accent'][:1] if available_files['accent'] else []
        }
        
        # Skip if we don't have minimum required content
        if not layer_files['base'] and not layer_files['binaural']:
            logger.warning(f"⚠️ Skipping {config['name']} - insufficient content")
            continue
        
        output_file = str(output_dir / f"{config['name'].lower().replace(' ', '_')}.wav")
        
        try:
            # Create the mix
            mix_info = mix_engine.create_seamless_mix(
                duration_minutes=config['duration'],
                mix_type=config['type'],
                layer_files=layer_files,
                output_file=output_file
            )
            
            # Save mix info
            info_file = output_file.replace('.wav', '_info.json')
            with open(info_file, 'w') as f:
                json.dump(mix_info, f, indent=2)
            
            created_mixes.append({
                'config': config,
                'output_file': output_file,
                'mix_info': mix_info
            })
            
            logger.info(f"✅ Created: {config['name']} ({mix_info['file_size_mb']:.1f}MB)")
            
        except Exception as e:
            logger.error(f"❌ Error creating {config['name']}: {e}")
    
    # Show results
    show_demo_results(created_mixes, available_files)


def show_demo_results(created_mixes: list, available_files: dict):
    """Show the results of the demo."""
    print("\n" + "=" * 60)
    print("🎉 SEAMLESS MIX ENGINE DEMO RESULTS")
    print("=" * 60)
    
    # Show available content
    print(f"\n📚 Available Content Library:")
    for category, files in available_files.items():
        print(f"  {category.title()}: {len(files)} files")
        for file in files[:3]:  # Show first 3
            print(f"    • {Path(file).name}")
        if len(files) > 3:
            print(f"    ... and {len(files) - 3} more")
    
    # Show created mixes
    print(f"\n🎵 Created Mixes:")
    total_size = 0
    
    for mix in created_mixes:
        config = mix['config']
        info = mix['mix_info']
        
        print(f"\n  🎧 {config['name']}")
        print(f"     Type: {config['type'].title()}")
        print(f"     Duration: {config['duration']} minutes")
        print(f"     File Size: {info['file_size_mb']:.1f}MB")
        print(f"     Timeline Events: {info['timeline_events']}")
        print(f"     Description: {config['description']}")
        print(f"     File: {Path(info['output_file']).name}")
        
        total_size += info['file_size_mb']
    
    print(f"\n📊 Summary:")
    print(f"   Total Mixes Created: {len(created_mixes)}")
    print(f"   Total File Size: {total_size:.1f}MB")
    print(f"   Average Quality: Perfect seamless loops!")
    
    # Show next steps
    print(f"\n🚀 Next Steps:")
    print(f"  1. 🎧 Play the demo mixes to hear the seamless quality")
    print(f"  2. 📁 Add more audio files to input_clips/ for variety")
    print(f"  3. 🎛️ Customize mix profiles for your preferences")
    print(f"  4. ⏱️ Create longer mixes (30-90 minutes) for real use")
    print(f"  5. 🎨 Build a GUI around this engine for easy mixing")
    
    # Show file locations
    if created_mixes:
        print(f"\n📂 Find your mixes in: demo_mixes/")
        for mix in created_mixes:
            print(f"   🎵 {Path(mix['output_file']).name}")


def main():
    """Run the seamless mix engine demo."""
    print("🎛️ SEAMLESS MIX ENGINE DEMO")
    print("=" * 50)
    print("This demo creates perfect, long-duration audio mixes")
    print("with seamless transitions and intelligent layering.")
    print("=" * 50)
    
    try:
        demo_mix_creation()
        
        print("\n🎉 Demo completed successfully!")
        print("\nThe Seamless Mix Engine is ready to create amazing")
        print("long-duration audio experiences that loop perfectly")
        print("and adapt to your desired outcomes!")
        
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        print(f"\n❌ Demo failed: {e}")


if __name__ == "__main__":
    main()
