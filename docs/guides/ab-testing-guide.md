# A/B Testing Guide

This guide explains how to use SonicSleep Pro's A/B testing system to systematically improve audio mixes based on user preferences.

## Overview

A/B testing is a method of comparing two versions of audio mixes to determine which one users prefer. The SonicSleep Pro A/B testing system automates this process by:

1. Creating variant mixes with controlled parameter differences
2. Collecting user preference data
3. Adjusting user profiles based on results
4. Using machine learning to optimize future mixes

## Core Components

The A/B testing system consists of two main classes:

- **ABTest**: Represents a single A/B test instance with variants and results
- **MixLearner**: Manages multiple tests and applies learning to user profiles

## Basic A/B Testing Workflow

### Step 1: Set Up the Environment

```python
from project_name.core.ab_testing import ABTest, MixLearner
from project_name.core.user_profile import UserProfile
from project_name.core.mix_creator import MixCreator
import os

# Initialize components
learner = MixLearner()
mixer = MixCreator(output_folder="ab_test_mixes")

# Create or load a user profile
profile = UserProfile(name="test_user", sleep_issue="insomnia")
learner.profiles[profile.name] = profile
```

### Step 2: Create an A/B Test

```python
# Create a test with automatically selected parameters
ab_test = learner.create_ab_test(profile.name)

print(f"Created A/B test: {ab_test.test_id}")
print(f"Testing parameter: {ab_test.test_parameter}")
print(f"Value for variant A: {ab_test.parameter_values['A']}")
print(f"Value for variant B: {ab_test.parameter_values['B']}")
```

### Step 3: Generate Mix Variants

```python
# Prepare audio files (assume we have processed audio files)
audio_files = {
    "rain": ["path/to/processed/rain1.wav", "path/to/processed/rain2.wav"],
    "thunder": ["path/to/processed/thunder.wav"],
    "white_noise": ["path/to/processed/white_noise.wav"]
}

# Create variant A
variant_a_path = mixer.create_mix(
    audio_files=audio_files,
    mix_type="sleep",
    duration_minutes=10,  # Shorter duration for testing
    **ab_test.variant_a_params
)

# Create variant B
variant_b_path = mixer.create_mix(
    audio_files=audio_files,
    mix_type="sleep",
    duration_minutes=10,
    **ab_test.variant_b_params
)

# Register mix paths in the test
ab_test.set_mix_paths(variant_a_path, variant_b_path)
```

### Step 4: Collect User Feedback

```python
# In a real application, you would present both variants to the user
# and collect their preference. Here we simulate a preference for variant A.
preferred_variant = "A"  # This would come from user input

# Optional detailed feedback
feedback = {
    "quality_rating": 8,
    "comments": "Preferred the more subtle rain sounds"
}

# Record the result
ab_test.record_result(preferred_variant, feedback)

# Calculate what we learned
parameter, delta = ab_test.get_learning_delta()
print(f"Learning: Adjust {parameter} by {delta}")
```

### Step 5: Update the User Profile

```python
# Update the learner with the test result
learner.record_ab_test_result(ab_test.test_id, preferred_variant, feedback)

# Save the test results
ab_test.save()

# The profile has been automatically updated through the learner
profile.save()
```

## Advanced A/B Testing Techniques

### Creating a Test with Specific Parameters

For more controlled experiments, you can create tests with specific parameters:

```python
# Create a test manually
test = ABTest("custom_test_id")

# Set up a specific parameter to test
test.setup_test(
    test_parameter="category_weights.rain",
    value_a=0.8,  # High rain weight
    value_b=0.3,  # Low rain weight
    base_params={
        "category_weights": {
            "thunder": 0.4,
            "white_noise": 0.5
        },
        "volume_preferences": {
            "base_sounds": -2,
            "occasional_sounds": -5
        }
    }
)

# Add the test to the learner
learner.ab_tests.append(test)
```

### Running Multiple Tests in Sequence

To gather more data points, you can run multiple tests in sequence:

```python
# Run a series of tests with different parameters
parameters_to_test = [
    "category_weights.rain",
    "category_weights.thunder",
    "eq_preferences.low",
    "volume_preferences.base_sounds"
]

test_results = {}

for param in parameters_to_test:
    # Create a test for this parameter
    test = learner.create_ab_test(profile.name)
    
    # Generate and present variants (simplified)
    variant_a_path = mixer.create_mix(audio_files, **test.variant_a_params)
    variant_b_path = mixer.create_mix(audio_files, **test.variant_b_params)
    test.set_mix_paths(variant_a_path, variant_b_path)
    
    # Collect preference (simulated)
    preferred_variant = "A"  # Would come from user
    
    # Record result
    learner.record_ab_test_result(test.test_id, preferred_variant)
    
    # Store test result
    test_results[param] = preferred_variant
```

### Analyzing Learning Trends

The system can analyze trends across multiple tests and users:

```python
# Analyze learning trends
trends = learner.analyze_learning_trends()

# Extract key insights
for category, data in trends["categories"].items():
    if data["count"] > 0:
        avg_weight = data["average_weight"]
        print(f"Category {category}: Average preferred weight = {avg_weight:.2f}")

# Check sleep issue specific trends
for issue, data in trends["sleep_issues"].items():
    if issue in trends["categories"]["rain"]["by_issue"]:
        issue_data = trends["categories"]["rain"]["by_issue"][issue]
        if issue_data["count"] > 0:
            issue_avg = issue_data["average_weight"]
            print(f"Rain preference for {issue}: {issue_avg:.2f}")
```

### Optimizing Parameters Based on Learning

Use the learning system to generate optimized parameters:

```python
# Get recommended parameters for a specific sleep issue
recommended = learner.get_recommended_parameters_for_sleep_issue("insomnia")

# Create a mix with the recommended parameters
optimized_mix = mixer.create_mix(
    audio_files=audio_files,
    mix_type="sleep",
    **recommended
)

print(f"Created optimized mix: {optimized_mix}")
```

## Best Practices

### Test Design

- **Isolate Variables**: Test one parameter at a time for clearer results
- **Sufficient Difference**: Ensure variants are different enough to be noticeable
- **Meaningful Parameters**: Focus on parameters that significantly impact the experience
- **Short Test Duration**: Use shorter mixes (5-10 minutes) for testing to reduce fatigue

### Collecting Feedback

- **Blind Testing**: Don't tell users which variant is which
- **Consistent Environment**: Have users test in their typical listening environment
- **Multiple Trials**: Run each test multiple times for statistical significance
- **Qualitative Comments**: Collect notes on why users preferred a variant

### Learning Application

- **Gradual Updates**: Apply learning in small increments to avoid overcorrection
- **Regular Testing**: Continue testing even after finding preferences
- **Cross-User Analysis**: Look for patterns across multiple users with similar sleep issues
- **Retesting**: Periodically retest parameters to confirm preferences haven't changed

## Troubleshooting

**Problem**: Test results seem inconsistent
**Solution**: Increase the difference between variants or run more tests

**Problem**: Learning doesn't seem to improve mixes
**Solution**: Check that the learning rate isn't too low; verify profiles are being saved

**Problem**: Users can't perceive differences between variants
**Solution**: Increase parameter deltas; focus on more perceptually significant parameters

## Next Steps

- Learn about the [Audio Processing Pipeline](audio-processing-pipeline.md) for more technical details
- Explore [User Profile Management](../examples/user-profile-management.md) for personalization
- Check out [Visualization Guide](visualization-guide.md) for representing A/B test results visually
