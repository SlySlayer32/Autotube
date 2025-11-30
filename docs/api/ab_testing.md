# ABTest API Reference

The `ABTest` class is responsible for managing A/B testing of sound mixes, allowing the system to learn user preferences through comparison of variants.

## Class Overview

```python
class ABTest:
    def __init__(self, test_id: Optional[str] = None)
    def setup_test(self, 
                  test_parameter: str, 
                  value_a: Any, 
                  value_b: Any, 
                  base_params: Optional[Dict] = None) -> None
    def record_result(self, 
                     preferred_variant: str, 
                     feedback: Optional[Dict] = None) -> None
    def get_learning_delta(self) -> Tuple[str, float]
    def set_mix_paths(self, 
                     variant_a_path: str, 
                     variant_b_path: str) -> None
    def save(self, folder_path: str = "ab_tests") -> str
    @classmethod
    def load(cls, file_path: str) -> 'ABTest'
```

## Constructor

### `__init__(test_id: Optional[str] = None)`

Initializes a new ABTest instance.

**Parameters:**

- `test_id` (str, optional): Unique identifier for the test. If not provided, a unique ID is generated based on current timestamp.

**Behavior:**

- Creates a new A/B test with empty parameters
- Sets creation timestamp
- Initializes tracking properties for test variants and results

**Example:**

```python
from project_name.core.ab_testing import ABTest

# Create with auto-generated ID
test = ABTest()
print(f"Created test: {test.test_id}")

# Create with custom ID
test = ABTest("custom_test_1")
print(f"Created test: {test.test_id}")
```

## Methods

### `setup_test(test_parameter: str, value_a: Any, value_b: Any, base_params: Optional[Dict] = None) -> None`

Configures the test with the parameter to test and values for each variant.

**Parameters:**

- `test_parameter` (str): The parameter name to test (e.g., "volume", "category_weights.rain")
- `value_a` (Any): The value for variant A

- `value_b` (Any): The value for variant B
- `base_params` (Dict, optional): Additional parameters to include in both variants

**Behavior:**

- Configures the parameter being tested and its values for each variant
- Creates variant parameter dictionaries with supplied values
- For nested parameters (using dot notation), correctly sets nested dictionary values

**Example:**

```python
# Test a simple parameter like volume
test.setup_test(
    test_parameter="volume",
    value_a=-3,  # -3dB for variant A
    value_b=0,   # 0dB for variant B
    base_params={"crossfade": 5000, "fade_in": 10000}
)

# Test a nested parameter like a category weight
test.setup_test(
    test_parameter="category_weights.rain",
    value_a=0.8,  # Higher rain weight for variant A
    value_b=0.4,  # Lower rain weight for variant B
    base_params={
        "category_weights": {
            "thunder": 0.3,  # Other parameters remain the same in both variants
            "white_noise": 0.5
        }
    }
)
```

### `record_result(preferred_variant: str, feedback: Optional[Dict] = None) -> None`

Records the user's preferred variant and optional feedback.

**Parameters:**

- `preferred_variant` (str): The user's preferred variant, either "A" or "B"
- `feedback` (Dict, optional): Additional feedback data such as comments or ratings

**Behavior:**

- Records which variant the user preferred
- Stores additional feedback information provided
- Sets result timestamp

**Example:**

```python
# Record basic preference
test.record_result("A")  # User preferred variant A

# Record preference with detailed feedback
test.record_result(
    preferred_variant="B",
    feedback={
        "rating": 8,
        "comments": "Preferred the lower volume version",
        "listened_duration": 120  # Seconds

    }
)
```

### `get_learning_delta(self) -> Tuple[str, float]`

Calculates the learning adjustment based on test results.

**Returns:**

- `Tuple[str, float]`: A tuple containing the parameter name and the adjustment value

**Behavior:**

- Based on the preferred variant, determines how to adjust the parameter
- Calculates an appropriate delta based on the difference between variants
- For nested parameters, returns the full parameter path

**Example:**

```python

# After recording a result
param, delta = test.get_learning_delta()

print(f"Learned: Adjust {param} by {delta}")

# Example output: "Learned: Adjust category_weights.rain by 0.15"
```

### `set_mix_paths(variant_a_path: str, variant_b_path: str) -> None`

Associates the test with the actual mix files created for each variant.

**Parameters:**

- `variant_a_path` (str): Path to the mix file for variant A
- `variant_b_path` (str): Path to the mix file for variant B

**Behavior:**

- Stores file paths to the actual audio mixes for later reference

**Example:**

```python

# After creating the mix files
test.set_mix_paths(
    variant_a_path="output_mixes/variant_a.mp3",

    variant_b_path="output_mixes/variant_b.mp3"
)
```

### `save(folder_path: str = "ab_tests") -> str`

Saves the test data to a JSON file.

**Parameters:**

- `folder_path` (str, optional): Directory where the test file should be saved. Default is "ab_tests".

**Returns:**

- `str`: Path to the saved test file

**Behavior:**

- Creates the folder if it doesn't exist
- Serializes test data to JSON format

- Saves with filename based on test_id

**Example:**

```python
# Save test to default location

saved_path = test.save()
print(f"Test saved to: {saved_path}")

# Save to a custom location

saved_path = test.save("my_ab_tests")
print(f"Test saved to: {saved_path}")
```

### `load(file_path: str) -> 'ABTest'`

Class method to load a test from a saved JSON file.

**Parameters:**

- `file_path` (str): Path to the saved test file

**Returns:**

- `ABTest`: Loaded ABTest instance

**Behavior:**

- Reads JSON file and deserializes to ABTest object
- Restores all test properties and results

**Example:**

```python
# Load a test from file
loaded_test = ABTest.load("ab_tests/abtest_test_user_1744433664.json")

print(f"Loaded test: {loaded_test.test_id}")
print(f"Test parameter: {loaded_test.test_parameter}")
print(f"Result: {loaded_test.result}")
```

## Properties

### `test_id`

Unique identifier for the test.

### `creation_time`

Timestamp when the test was created.

### `test_parameter`

The parameter being tested (e.g., "volume", "category_weights.rain").

### `parameter_values`

Dictionary mapping variant names ("A" and "B") to their values for the test parameter.

### `variant_a_params`

Complete parameter dictionary for variant A, including base parameters.

### `variant_b_params`

Complete parameter dictionary for variant B, including base parameters.

### `result`

The preferred variant after recording a result ("A", "B", or None).

### `feedback`

Dictionary containing any additional feedback provided with the result.

### `result_time`

Timestamp when the result was recorded (None if no result recorded).

### `variant_a_mix_path`

Path to the audio file for variant A (if set).

### `variant_b_mix_path`

Path to the audio file for variant B (if set).

## Usage Notes

- The ABTest class is designed to test one parameter at a time for clear results
- For nested parameters, use dot notation (e.g., "category_weights.rain")
- When working with many A/B tests, use the MixLearner class to manage them
- Best practice is to use significant differences between variants so users can clearly perceive differences
- Parameters that can be tested include:
  - Category weights (e.g., "category_weights.rain")
  - EQ preferences (e.g., "eq_preferences.low")
  - Volume preferences (e.g., "volume_preferences.base_sounds")
  - Crossfade durations (e.g., "crossfade")
  - Effect settings (e.g., "reverb_level")
