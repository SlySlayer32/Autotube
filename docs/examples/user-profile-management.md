# User Profile Management Example

This example demonstrates how to use SonicSleep Pro's user profile system to create personalized mixes based on user preferences and sleep needs.

## Overview

In this example, we'll:

1. Create and configure user profiles
2. Load existing profiles
3. Update profiles based on user feedback
4. Create personalized mixes
5. Save and manage profile data

## Complete Example

```python
"""
User Profile Management Example for SonicSleep Pro

This script demonstrates how to work with user profiles for
personalized audio mix creation.
"""

import os
from pathlib import Path
import json
from project_name.core.user_profile import UserProfile
from project_name.core.mix_creator import MixCreator
from project_name.core.processor import SoundProcessor

def main():
    # Set up directories
    profiles_dir = "user_profiles"
    output_dir = "output_mixes"
    
    os.makedirs(profiles_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    # Step 1: Create a new user profile
    print("Creating a new user profile...")
    profile = UserProfile(
        name="alex",
        sleep_issue="insomnia"  # Other options: "light_sleep", "nightmares", None
    )
    
    print(f"Created profile for {profile.name} with sleep issue: {profile.sleep_issue}")
    print(f"Initial category weights: {json.dumps(profile.category_weights, indent=2)}")
    
    # Step 2: Customize profile preferences
    print("\nCustomizing profile preferences...")
    
    # Update category weights
    profile.category_weights["rain"] = 0.8       # Strong preference for rain
    profile.category_weights["thunder"] = 0.2    # Light preference for thunder
    
    # Update EQ preferences
    profile.eq_preferences["low"] = 3            # Boost bass frequencies
    profile.eq_preferences["high"] = -2          # Reduce high frequencies
    
    # Update volume preferences
    profile.volume_preferences["base_sounds"] = -2     # Base sounds slightly quieter
    profile.volume_preferences["occasional_sounds"] = -8  # Occasional sounds much quieter
    
    # Add preferred sounds
    profile.preferred_sounds = ["rain_medium.wav", "soft_thunder.wav"]
    
    # Add avoided sounds
    profile.avoided_sounds = ["heavy_thunder.wav", "city_traffic.wav"]
    
    print("Profile preferences updated.")
    
    # Step 3: Save the profile
    profile_path = profile.save(profiles_dir)
    print(f"Profile saved to: {profile_path}")
    
    # Step 4: Load an existing profile
    print("\nLoading profile from file...")
    loaded_profile = UserProfile.load(profile_path)
    print(f"Loaded profile for {loaded_profile.name}")
    
    # Step 5: Create a personalized mix based on the profile
    print("\nCreating a personalized mix...")
    
    # Initialize components
    processor = SoundProcessor()
    mixer = MixCreator(output_folder=output_dir)
    
    # Get processed files
    processed_files = processor.process_batch()
    
    # Organize audio files by category
    audio_files = {
        "rain": [f for f in processed_files if "rain" in f.lower()],
        "thunder": [f for f in processed_files if "thunder" in f.lower()]
    }
    
    # Filter out avoided sounds
    for category, files in audio_files.items():
        audio_files[category] = [
            f for f in files 
            if not any(avoided in f for avoided in loaded_profile.avoided_sounds)
        ]
    
    # Prioritize preferred sounds
    for category, files in audio_files.items():
        # Move preferred sounds to the front of the list
        preferred = [f for f in files if any(preferred in f for preferred in loaded_profile.preferred_sounds)]
        other = [f for f in files if not any(preferred in f for preferred in loaded_profile.preferred_sounds)]
        audio_files[category] = preferred + other
    
    # Filter categories based on weights
    audio_files = {
        category: files 
        for category, files in audio_files.items() 
        if loaded_profile.category_weights.get(category, 0) > 0.2 and files
    }
    
    # Create a mix with the profile's preferences
    mix_path = mixer.create_mix(
        audio_files=audio_files,
        mix_type="sleep",
        duration_minutes=30,
        # Apply profile-specific parameters
        eq_settings={
            "low": loaded_profile.eq_preferences["low"],
            "mid": loaded_profile.eq_preferences["mid"],
            "high": loaded_profile.eq_preferences["high"]
        },
        volume_adjustments={
            "base": loaded_profile.volume_preferences["base_sounds"],
            "occasional": loaded_profile.volume_preferences["occasional_sounds"]
        }
    )
    
    print(f"Personalized mix created at: {mix_path}")
    
    # Step 6: Update profile based on feedback
    print("\nUpdating profile based on feedback...")
    
    # Simulate user feedback (1-10 scale)
    feedback_score = 8  # High satisfaction
    
    # Record the mix parameters
    mix_params = {
        "category_weights": loaded_profile.category_weights,
        "primary_sounds": ["rain_medium.wav"],
        "eq_preferences": loaded_profile.eq_preferences
    }
    
    # Update profile with feedback
    loaded_profile.update_from_feedback(
        mix_id=os.path.basename(mix_path),
        feedback_score=feedback_score,
        mix_params=mix_params
    )
    
    print(f"Profile updated with feedback score: {feedback_score}")
    print(f"Updated category weights: {json.dumps(loaded_profile.category_weights, indent=2)}")
    
    # Check which sounds are now preferred
    print(f"Preferred sounds: {loaded_profile.preferred_sounds}")
    
    # Save the updated profile
    updated_path = loaded_profile.save(profiles_dir)
    print(f"Updated profile saved to: {updated_path}")
    
    # Step 7: Demonstrate profile for different sleep issues
    print("\nCreating profiles for different sleep issues...")
    
    # Create profiles for different sleep issues
    profiles = {
        "insomnia": UserProfile(name="user1", sleep_issue="insomnia"),
        "light_sleep": UserProfile(name="user2", sleep_issue="light_sleep"),
        "nightmares": UserProfile(name="user3", sleep_issue="nightmares"),
        "general": UserProfile(name="user4", sleep_issue=None)
    }
    
    # Compare category weights across different profiles
    print("\nCategory weight comparison by sleep issue:")
    for issue, p in profiles.items():
        rain_weight = p.category_weights.get("rain", 0)
        thunder_weight = p.category_weights.get("thunder", 0)
        white_noise_weight = p.category_weights.get("white_noise", 0)
        
        print(f"{issue}: rain={rain_weight:.2f}, thunder={thunder_weight:.2f}, white_noise={white_noise_weight:.2f}")

if __name__ == "__main__":
    main()
```

## Running the Example

Save this code to a file (e.g., `user_profile_example.py`) and run it:

```bash
python user_profile_example.py
```

## Step-by-Step Explanation

### 1. Creating a User Profile

We start by creating a user profile with:

- A name identifier
- A sleep issue type (which affects initial preferences)

The `UserProfile` constructor automatically sets default preferences based on the sleep issue:

- Insomnia: Emphasizes white noise and rain, reduces occasional sounds
- Light sleep: Balanced sound profile with minimal variations
- Nightmares: Emphasizes soothing sounds, minimizes sudden changes
- None (general): Neutral starting point

### 2. Customizing Preferences

We customize the profile with specific preferences:

- Category weights: How much of each sound category to include
- EQ preferences: Frequency balance adjustments
- Volume preferences: Relative volume levels for different sound types
- Preferred sounds: Specific audio files the user likes
- Avoided sounds: Specific audio files the user dislikes

### 3. Saving and Loading Profiles

Profiles can be:

- Saved to disk as JSON files
- Loaded from previously saved files

This persistence allows user preferences to be maintained across sessions.

### 4. Creating Personalized Mixes

We use the profile to create a personalized mix by:

- Filtering out avoided sounds
- Prioritizing preferred sounds
- Selecting categories based on weights
- Applying the profile's EQ and volume preferences

### 5. Feedback and Learning

The system learns from user feedback:

- Feedback score (1-10) indicates satisfaction
- The profile is updated based on this feedback
- Weights for successful elements are increased
- Successful sounds are added to preferred sounds

### 6. Sleep Issue Comparison

Different sleep issues have different default preferences:

- Insomnia: Focuses on consistent, masking sounds
- Light sleep: Balanced approach with minimal variation
- Nightmares: Soothing sounds with gradual transitions
- General: Neutral starting point

## Profile Properties

### Core Properties

- `name`: User identifier
- `sleep_issue`: Type of sleep issue (affects default preferences)
- `creation_date`: When the profile was created

### Preference Properties

- `category_weights`: Relative importance of each sound category
- `eq_preferences`: Equalizer settings (low, mid, high frequencies)
- `volume_preferences`: Volume settings for different sound types
- `preferred_sounds`: List of specific sound files the user likes
- `avoided_sounds`: List of specific sound files the user dislikes

### Learning Properties

- `mix_feedback`: Dictionary mapping mix IDs to feedback scores
- `ab_test_results`: Dictionary mapping A/B test IDs to preferred variants

## Advanced Profile Usage

### Creating a Profile with Custom Initial Weights

```python
# Create a profile with custom initial category weights
custom_profile = UserProfile(
    name="custom_user",
    sleep_issue=None,  # No specific sleep issue
    initial_weights={
        "rain": 0.9,
        "ocean": 0.8,
        "white_noise": 0.3,
        "thunder": 0.0  # No thunder at all
    }
)
```

### Managing Multiple Profiles

```python
# Load all profiles from a directory
def load_all_profiles(profiles_dir):
    profiles = {}
    for file in os.listdir(profiles_dir):
        if file.endswith(".json"):
            path = os.path.join(profiles_dir, file)
            profile = UserProfile.load(path)
            profiles[profile.name] = profile
    return profiles

# Usage
all_profiles = load_all_profiles("user_profiles")
for name, profile in all_profiles.items():
    print(f"Profile: {name}, Sleep Issue: {profile.sleep_issue}")
```

### Profile Evolution Analysis

```python
# Track how a profile evolves over time
def analyze_profile_evolution(profile, num_mixes=10):
    """Simulate profile evolution over multiple feedback iterations."""
    initial_weights = profile.category_weights.copy()
    
    # Simulate creating mixes and getting feedback
    for i in range(num_mixes):
        # Create a mix (simplified)
        mix_id = f"mix_{i}"
        
        # Simulate positive feedback for rain
        mix_params = {
            "category_weights": profile.category_weights,
            "primary_sounds": ["rain_medium.wav"],
        }
        
        # Update profile with feedback
        profile.update_from_feedback(
            mix_id=mix_id,
            feedback_score=8,  # High satisfaction
            mix_params=mix_params
        )
    
    # Compare initial and final weights
    print("Category weight evolution:")
    for category, initial in initial_weights.items():
        final = profile.category_weights.get(category, 0)
        change = final - initial
        print(f"  {category}: {initial:.2f} → {final:.2f} (Δ: {change:+.2f})")

# Usage
test_profile = UserProfile(name="evolution_test")
analyze_profile_evolution(test_profile)
```

## Next Steps

- Learn about [A/B Testing](../guides/ab-testing-guide.md) to systematically improve profiles
- Explore [Basic Mix Creation](basic-mix-creation.md) for more mixing options
- Check out [Audio Processing Pipeline](../guides/audio-processing-pipeline.md) for technical details
