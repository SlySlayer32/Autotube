# Core API Reference

This document provides an overview of the SonicSleep Pro core API, describing the main classes, their relationships, and primary functionalities.

## Core Components Overview

The SonicSleep Pro API consists of several core components that work together to create personalized audio mixes. The following diagram shows the relationships between these components:

```
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│ SoundProcessor│────▶│   MixCreator  │◀────│  UserProfile  │
└───────────────┘     └───────────────┘     └───────────────┘
        │                     │                     ▲
        │                     │                     │
        │                     ▼                     │
        │              ┌───────────────┐            │
        └─────────────▶│ AudioVisualizer│           │
                       └───────────────┘            │
                                                    │
                      ┌───────────────┐             │
                      │    ABTest     │─────────────┘
                      └───────────────┘
                             ▲
                             │
                      ┌───────────────┐
                      │   MixLearner  │
                      └───────────────┘
```

## Core Classes

### SoundProcessor

Responsible for processing audio files, normalizing them, and preparing them for mixing.

**Key Features:**

- Audio file normalization
- Silence trimming
- Audio effect application (EQ, compression, etc.)
- Batch processing

[Detailed SoundProcessor documentation](processor.md)

### MixCreator

Creates audio mixes by combining multiple sound files according to specified parameters.

**Key Features:**

- Creating full-length mixes
- Generating previews
- Applying different mix profiles (sleep, focus, relax)
- Customizable export options

[Detailed MixCreator documentation](mix_creator.md)

### UserProfile

Stores user preferences and feedback for personalized mix creation.

**Key Features:**

- Sleep issue profiles
- Sound preferences
- Category weight management
- Preference learning from feedback

[Detailed UserProfile documentation](user_profile.md)

### ABTest

Facilitates A/B testing to determine user preferences between different mix variants.

**Key Features:**

- Test parameter configuration
- Result recording
- Learning delta calculation
- Persistence (save/load)

[Detailed ABTest documentation](ab_testing.md)

### MixLearner

Uses machine learning techniques to optimize mix parameters based on user feedback and A/B testing.

**Key Features:**

- Profile management
- A/B test creation and analysis
- Parameter optimization
- Learning trend analysis

[Detailed MixLearner documentation](deep_learning.md)

### AudioVisualizer

Provides visualization tools for audio analysis and representation.

**Key Features:**

- Waveform visualization
- Spectrogram generation
- Mix composition visualization
- Analysis report generation

[Detailed AudioVisualizer documentation](visualizer.md)

## Common Workflows

### Basic Mix Creation Workflow

```python
# Initialize components
processor = SoundProcessor()
mixer = MixCreator()

# Process audio files
processed_files = processor.process_batch()

# Organize files by category
audio_files = {
    "rain": [...],
    "thunder": [...],
    # Other categories
}

# Create mix
mix_path = mixer.create_mix(audio_files, mix_type="sleep")
```

### Personalized Mix Creation Workflow

```python
# Initialize components
processor = SoundProcessor()
mixer = MixCreator()
profile = UserProfile(name="user1", sleep_issue="insomnia")
learner = MixLearner()

# Add profile to learner
learner.profiles[profile.name] = profile

# Get optimized parameters
params = learner.optimize_mix_parameters(profile.name)

# Create mix with optimized parameters
mix_path = mixer.create_mix(audio_files, **params)

# Record feedback
profile.update_from_feedback("mix_id", 8, params)
```

### A/B Testing Workflow

```python
# Initialize components
learner = MixLearner()
profile = UserProfile(name="user1")
learner.profiles[profile.name] = profile

# Create A/B test
ab_test = learner.create_ab_test(profile.name)

# Record test result
learner.record_ab_test_result(ab_test.test_id, "A")
```

## Common Data Structures

### Audio Files Dictionary

```python
audio_files = {
    "category1": ["path/to/file1.wav", "path/to/file2.wav"],
    "category2": ["path/to/file3.wav"]
}
```

### Mix Parameters

```python
mix_params = {
    "category_weights": {
        "rain": 0.7,
        "thunder": 0.3,
        "white_noise": 0.5
    },
    "eq_preferences": {
        "low": 2,
        "mid": 0,
        "high": -1
    },
    "volume_preferences": {
        "base_sounds": 0,
        "occasional_sounds": -3
    }
}
```

### Mix Profiles

```python
mix_profile = {
    "fade_in": 10000,  # milliseconds
    "fade_out": 10000,
    "crossfade": 5000,
    "volume_adjustments": {
        "rain": 0,
        "thunder": -6
    },
    "low_pass": 4000  # Hz
}
```

## Error Handling

Most API methods return `None` or `False` if an error occurs, and log the error using the Python `logging` module. For more robust error handling, you can wrap API calls in try/except blocks:

```python
try:
    result = mixer.create_mix(audio_files)
    if result is None:
        print("Mix creation failed, check logs for details")
    else:
        print(f"Mix created successfully: {result}")
except Exception as e:
    print(f"Error creating mix: {str(e)}")
```

## Logging

The SonicSleep Pro API uses the standard Python `logging` module. You can configure the logging level and handlers to capture logs:

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='sonicsleep.log'
)

# Create logger
logger = logging.getLogger('sonicsleep')
```

## Thread Safety

The core API classes are not thread-safe by default. If you need to use them in a multi-threaded environment, you should ensure appropriate synchronization or create separate instances for each thread.
