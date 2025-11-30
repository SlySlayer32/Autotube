import json
import logging
import os
import random
import time
from pathlib import Path  # Added missing import
from typing import Any, Dict, Tuple

from project_name.core.user_profile import UserProfile

logger = logging.getLogger(__name__)


class ABTest:
    """
    Class to manage A/B testing of sound mixes
    """

    def __init__(self, test_id: str = None):
        """
        Initialize an A/B test

        Args:
            test_id: Optional ID for the test
        """
        self.test_id = test_id or f"abtest_{int(time.time())}"
        self.creation_time = time.time()
        self.test_parameter = None  # Parameter being tested
        self.parameter_values = {}  # Values for A and B variants
        self.variant_a_params = {}  # Full parameters for variant A
        self.variant_b_params = {}  # Full parameters for variant B
        self.variant_a_path = None  # Path to variant A mix
        self.variant_b_path = None  # Path to variant B mix
        self.result = None  # Which variant was preferred ('A', 'B', or None)
        self.feedback = {}  # Optional detailed feedback

    def setup_test(
        self, test_parameter: str, value_a: Any, value_b: Any, base_params: Dict = None
    ) -> None:
        """
        Set up the test with parameters to vary

        Args:
            test_parameter: Parameter to test (e.g., "primary_category", "eq_settings")
            value_a: Value for variant A
            value_b: Value for variant B
            base_params: Base parameters for both variants
        """
        self.test_parameter = test_parameter
        self.parameter_values = {"A": value_a, "B": value_b}

        # Set up full parameters for each variant
        self.variant_a_params = base_params.copy() if base_params else {}
        self.variant_b_params = base_params.copy() if base_params else {}

        # Add test parameter to each variant
        if test_parameter.startswith("category_weights."):
            # Handle nested parameters
            category = test_parameter.split(".")[1]
            if "category_weights" not in self.variant_a_params:
                self.variant_a_params["category_weights"] = {}
                self.variant_b_params["category_weights"] = {}
            self.variant_a_params["category_weights"][category] = value_a
            self.variant_b_params["category_weights"][category] = value_b
        else:
            # Simple parameter
            self.variant_a_params[test_parameter] = value_a
            self.variant_b_params[test_parameter] = value_b

        logger.info(f"Set up A/B test {self.test_id} for parameter '{test_parameter}'")
        logger.info(f"Variant A: {value_a}")
        logger.info(f"Variant B: {value_b}")

    def set_mix_paths(self, variant_a_path: str, variant_b_path: str) -> None:
        """
        Set the file paths for the A/B test mixes

        Args:
            variant_a_path: Path to variant A mix
            variant_b_path: Path to variant B mix
        """
        self.variant_a_path = variant_a_path
        self.variant_b_path = variant_b_path
        logger.info(f"Set mix paths for A/B test {self.test_id}")

    def record_result(self, preferred_variant: str, feedback: Dict = None) -> None:
        """
        Record the result of the A/B test

        Args:
            preferred_variant: The preferred variant ('A' or 'B')
            feedback: Optional feedback details
        """
        self.result = preferred_variant
        if feedback:
            self.feedback = feedback

        logger.info(
            f"Recorded result for A/B test {self.test_id}: preferred variant {preferred_variant}"
        )

    def get_learning_delta(self) -> Tuple[str, float]:
        """
        Calculate what we learned from this test

        Returns:
            Tuple of (parameter, adjustment value)
        """
        if not self.result:
            return (None, 0.0)

        # Simplified assumption: the difference between values indicates the adjustment
        if self.test_parameter and self.result in ("A", "B"):
            try:
                # For numeric values, calculate a weighted average difference
                value_a = self.parameter_values["A"]
                value_b = self.parameter_values["B"]

                if isinstance(value_a, (int, float)) and isinstance(
                    value_b, (int, float)
                ):
                    # If the preferred variant is A, we want to move toward value_a
                    # If the preferred variant is B, we want to move toward value_b
                    direction = 1.0 if self.result == "A" else -1.0
                    delta = (value_a - value_b) * 0.3 * direction  # 30% adjustment
                    return (self.test_parameter, delta)
                else:
                    # For non-numeric values, just return the preferred value
                    return (self.test_parameter, self.parameter_values[self.result])
            except Exception as e:
                logger.error(
                    f"Error calculating learning delta for test {self.test_id}: {str(e)}"
                )

        return (None, 0.0)

    def save(
        self, folder_path: str = "ab_tests"
    ) -> Path:  # Changed return type hint to Path
        """
        Save the A/B test to a file

        Args:
            folder_path: Folder to save test in

        Returns:
            Path to saved test file
        """
        os.makedirs(folder_path, exist_ok=True)

        # Create filename
        filename = f"{self.test_id}.json"
        file_path = os.path.join(folder_path, filename)

        # Convert to dict for serialization
        test_data = {
            "test_id": self.test_id,
            "creation_time": self.creation_time,
            "test_parameter": self.test_parameter,
            "parameter_values": self.parameter_values,
            "variant_a_params": self.variant_a_params,
            "variant_b_params": self.variant_b_params,
            "variant_a_path": self.variant_a_path,
            "variant_b_path": self.variant_b_path,
            "result": self.result,
            "feedback": self.feedback,
        }

        # Save to file
        with open(file_path, "w") as f:
            json.dump(test_data, f, indent=2)

        logger.info(f"Saved A/B test to {file_path}")
        return Path(file_path)  # Return Path object

    @classmethod
    def load(cls, file_path: str) -> "ABTest":
        """
        Load an A/B test from file

        Args:
            file_path: Path to test file

        Returns:
            Loaded ABTest object
        """
        try:
            with open(file_path, "r") as f:
                test_data = json.load(f)

            # Create new test instance
            test = cls(test_id=test_data.get("test_id"))

            # Load attributes
            test.creation_time = test_data.get("creation_time", time.time())
            test.test_parameter = test_data.get("test_parameter")
            test.parameter_values = test_data.get("parameter_values", {})
            test.variant_a_params = test_data.get("variant_a_params", {})
            test.variant_b_params = test_data.get("variant_b_params", {})
            test.variant_a_path = test_data.get("variant_a_path")
            test.variant_b_path = test_data.get("variant_b_path")
            test.result = test_data.get("result")
            test.feedback = test_data.get("feedback", {})

            return test

        except Exception as e:
            logger.error(f"Error loading A/B test from {file_path}: {str(e)}")
            return cls()  # Return a new empty test instance as fallback


class MixLearner:
    """
    Class that implements the learning algorithm for personalized mixes
    based on user feedback and A/B testing
    """

    def __init__(self):
        """Initialize the learning algorithm"""
        self.profiles = {}  # User name to UserProfile
        self.ab_tests = []  # List of ABTest objects
        self.learning_rate = 0.1  # How quickly we adjust parameters based on feedback
        self.test_parameters = [  # Parameters that can be tested
            "category_weights.rain",
            "category_weights.thunder",
            "category_weights.white_noise",
            "category_weights.nature",
            "category_weights.water",
            "eq_preferences.low",
            "eq_preferences.mid",
            "eq_preferences.high",
            "volume_preferences.base_sounds",
            "volume_preferences.occasional_sounds",
        ]

    def load_profiles(self, folder_path: str = "user_profiles") -> None:
        """
        Load all user profiles from a folder

        Args:
            folder_path: Folder containing profile files
        """
        if not os.path.exists(folder_path):
            logger.info(f"Profile folder {folder_path} doesn't exist, creating it")
            os.makedirs(folder_path, exist_ok=True)
            return

        profile_files = [
            f for f in os.listdir(folder_path) if f.endswith("_profile.json")
        ]

        for profile_file in profile_files:
            try:
                file_path = os.path.join(folder_path, profile_file)
                profile = UserProfile.load(file_path)
                self.profiles[profile.name] = profile
                logger.info(f"Loaded profile: {profile.name}")
            except Exception as e:
                logger.error(f"Error loading profile {profile_file}: {str(e)}")

        logger.info(f"Loaded {len(self.profiles)} user profiles")

    def load_ab_tests(self, folder_path: str = "ab_tests") -> None:
        """
        Load all A/B tests from a folder

        Args:
            folder_path: Folder containing test files
        """
        if not os.path.exists(folder_path):
            logger.info(f"A/B test folder {folder_path} doesn't exist, creating it")
            os.makedirs(folder_path, exist_ok=True)
            return

        test_files = [f for f in os.listdir(folder_path) if f.endswith(".json")]

        for test_file in test_files:
            try:
                file_path = os.path.join(folder_path, test_file)
                test = ABTest.load(file_path)
                self.ab_tests.append(test)
                logger.info(f"Loaded A/B test: {test.test_id}")
            except Exception as e:
                logger.error(f"Error loading A/B test {test_file}: {str(e)}")

        logger.info(f"Loaded {len(self.ab_tests)} A/B tests")

    def get_profile(self, user_name: str, sleep_issue: str = None) -> UserProfile:
        """
        Get a user profile, creating it if it doesn't exist

        Args:
            user_name: Name of the user
            sleep_issue: Optional sleep issue type

        Returns:
            UserProfile for the user
        """
        if user_name in self.profiles:
            return self.profiles[user_name]

        # Create new profile
        profile = UserProfile(name=user_name, sleep_issue=sleep_issue)
        self.profiles[user_name] = profile

        # Save the new profile
        profile.save()
        logger.info(f"Created new profile for user {user_name}")

        return profile

    def create_ab_test(self, user_name: str, base_params: Dict = None) -> ABTest:
        """
        Create a new A/B test for a user

        Args:
            user_name: Name of the user
            base_params: Base parameters for both variants

        Returns:
            ABTest object
        """
        # Get user profile
        profile = self.get_profile(user_name)

        # Create test ID
        test_id = f"abtest_{user_name}_{int(time.time())}"

        # Create A/B test
        ab_test = ABTest(test_id=test_id)

        # Choose a parameter to test
        test_parameter = random.choice(self.test_parameters)

        # Set parameter values based on current profile preferences
        if test_parameter.startswith("category_weights."):
            # Testing a category weight
            category = test_parameter.split(".")[1]
            current_value = profile.category_weights.get(category, 0.5)

            # Create two variants that differ by 20-30%
            delta = random.uniform(0.2, 0.3)
            value_a = max(0.1, min(0.9, current_value + delta))
            value_b = max(0.1, min(0.9, current_value - delta))

        elif test_parameter.startswith("eq_preferences."):
            # Testing an EQ preference
            band = test_parameter.split(".")[1]
            current_value = profile.eq_preferences.get(band, 0)

            # Create two variants that differ by 2-4 dB
            delta = random.uniform(2, 4)
            value_a = current_value + delta
            value_b = current_value - delta

        elif test_parameter.startswith("volume_preferences."):
            # Testing a volume preference
            key = test_parameter.split(".")[1]
            current_value = profile.volume_preferences.get(key, 0)

            # Create two variants that differ by 2-4 dB
            delta = random.uniform(2, 4)
            value_a = current_value + delta
            value_b = current_value - delta

        else:
            # Generic numeric parameter
            # Default to testing between 0.3 and 0.7
            value_a = 0.7
            value_b = 0.3

        # Set up test
        if not base_params:
            base_params = {}

        # Add current profile preferences to base params
        base_params["category_weights"] = profile.category_weights.copy()
        base_params["eq_preferences"] = profile.eq_preferences.copy()
        base_params["volume_preferences"] = profile.volume_preferences.copy()

        ab_test.setup_test(test_parameter, value_a, value_b, base_params)

        # Add to test list
        self.ab_tests.append(ab_test)

        # Save the test
        ab_test.save()

        logger.info(
            f"Created A/B test {test_id} for user {user_name}, testing {test_parameter}"
        )
        return ab_test

    def record_ab_test_result(
        self, test_id: str, preferred_variant: str, feedback: Dict = None
    ) -> None:
        """
        Record the result of an A/B test and update user profile

        Args:
            test_id: ID of the test
            preferred_variant: The preferred variant ('A' or 'B')
            feedback: Optional feedback details
        """
        # Find the test
        for test in self.ab_tests:
            if test.test_id == test_id:
                # Record result in test
                test.record_result(preferred_variant, feedback)
                test.save()  # Save updated test

                # Extract user name from test ID (format: abtest_username_timestamp)
                parts = test_id.split("_")
                if len(parts) >= 3:
                    user_name = parts[1]

                    # Update user profile if we have one
                    if user_name in self.profiles:
                        profile = self.profiles[user_name]
                        profile.update_from_ab_test(
                            test_id,
                            preferred_variant,
                            test.variant_a_params,
                            test.variant_b_params,
                        )
                        profile.save()  # Save updated profile

                        logger.info(
                            f"Updated profile for {user_name} based on A/B test {test_id}"
                        )

                logger.info(
                    f"Recorded result for A/B test {test_id}: preferred variant {preferred_variant}"
                )
                return

        logger.warning(f"A/B test {test_id} not found")

    def record_mix_feedback(
        self, user_name: str, mix_id: str, feedback_score: int, mix_params: Dict
    ) -> None:
        """
        Record feedback for a mix and update user profile

        Args:
            user_name: Name of the user
            mix_id: ID of the mix
            feedback_score: User feedback score (1-10)
            mix_params: Parameters used to create the mix
        """
        # Get user profile
        profile = self.get_profile(user_name)

        # Update profile based on feedback
        profile.update_from_feedback(mix_id, feedback_score, mix_params)

        # Save profile
        profile.save()

        logger.info(
            f"Recorded feedback (score: {feedback_score}) for mix {mix_id} from user {user_name}"
        )

    def optimize_mix_parameters(self, user_name: str, base_params: Dict = None) -> Dict:
        """
        Optimize mix parameters for a user based on their profile

        Args:
            user_name: Name of the user
            base_params: Optional base parameters

        Returns:
            Optimized parameters for creating a mix
        """
        # Get user profile
        profile = self.get_profile(user_name)

        # Start with base params or empty dict
        optimized_params = base_params.copy() if base_params else {}

        # Apply profile preferences

        # Category weights
        optimized_params["category_weights"] = profile.category_weights.copy()

        # EQ preferences
        optimized_params["eq_preferences"] = profile.eq_preferences.copy()

        # Volume preferences
        optimized_params["volume_preferences"] = profile.volume_preferences.copy()

        # Sound preferences
        optimized_params["preferred_sounds"] = profile.preferred_sounds.copy()
        optimized_params["avoided_sounds"] = profile.avoided_sounds.copy()

        # Duration preference
        if "duration" not in optimized_params:
            optimized_params["duration"] = profile.preferred_duration

        logger.info(
            f"Optimized mix parameters for user {user_name} based on their profile"
        )
        return optimized_params

    def analyze_learning_trends(self) -> Dict:
        """
        Analyze learning trends across all users and tests

        Returns:
            Dictionary with trend analysis
        """
        trends = {"parameters": {}, "categories": {}, "sleep_issues": {}}

        # Analyze profile trends
        for name, profile in self.profiles.items():
            # Count by sleep issue
            sleep_issue = profile.sleep_issue or "unknown"
            if sleep_issue not in trends["sleep_issues"]:
                trends["sleep_issues"][sleep_issue] = 0
            trends["sleep_issues"][sleep_issue] += 1

            # Analyze category preferences by sleep issue
            for category, weight in profile.category_weights.items():
                if category not in trends["categories"]:
                    trends["categories"][category] = {
                        "total_weight": 0.0,
                        "count": 0,
                        "by_issue": {},
                    }

                # Add to overall stats
                trends["categories"][category]["total_weight"] += weight
                trends["categories"][category]["count"] += 1

                # Add to per-issue stats
                if sleep_issue not in trends["categories"][category]["by_issue"]:
                    trends["categories"][category]["by_issue"][sleep_issue] = {
                        "total_weight": 0.0,
                        "count": 0,
                    }

                trends["categories"][category]["by_issue"][sleep_issue][
                    "total_weight"
                ] += weight
                trends["categories"][category]["by_issue"][sleep_issue]["count"] += 1

        # Calculate averages for categories
        for category, data in trends["categories"].items():
            if data["count"] > 0:
                data["average_weight"] = data["total_weight"] / data["count"]

            # Calculate averages by sleep issue
            for issue, issue_data in data["by_issue"].items():
                if issue_data["count"] > 0:
                    issue_data["average_weight"] = (
                        issue_data["total_weight"] / issue_data["count"]
                    )

        # Analyze A/B test trends
        parameter_tests = {}
        for test in self.ab_tests:
            if test.result and test.test_parameter:
                if test.test_parameter not in parameter_tests:
                    parameter_tests[test.test_parameter] = {
                        "total_tests": 0,
                        "preference_a": 0,
                        "preference_b": 0,
                    }

                parameter_tests[test.test_parameter]["total_tests"] += 1
                if test.result == "A":
                    parameter_tests[test.test_parameter]["preference_a"] += 1
                elif test.result == "B":
                    parameter_tests[test.test_parameter]["preference_b"] += 1

        trends["parameters"] = parameter_tests

        # Calculate most effective sounds for each sleep issue
        if trends["sleep_issues"]:
            effective_sounds_by_issue = {}

            for name, profile in self.profiles.items():
                sleep_issue = profile.sleep_issue or "unknown"

                # Skip if no feedback
                if not profile.mix_feedback:
                    continue

                if sleep_issue not in effective_sounds_by_issue:
                    effective_sounds_by_issue[sleep_issue] = {}

                # Analyze feedback for each mix
                for mix_id, score in profile.mix_feedback.items():
                    # Only consider mixes with positive feedback
                    if score >= 7:
                        # We'd need to store the sounds used in each mix to do this properly
                        # For now we'll just use dummy data
                        pass

            # Calculate average scores
            for issue, sounds in effective_sounds_by_issue.items():
                for sound, data in sounds.items():
                    if data["count"] > 0:
                        data["average_score"] = data["total_score"] / data["count"]

            trends["effective_sounds_by_issue"] = effective_sounds_by_issue

        return trends

    def get_recommended_parameters_for_sleep_issue(self, sleep_issue: str) -> Dict:
        """
        Get recommended parameters for a specific sleep issue
        based on learning from all users with that issue

        Args:
            sleep_issue: Type of sleep issue

        Returns:
            Dictionary of recommended parameters
        """
        # Analyze trends
        trends = self.analyze_learning_trends()

        # Default parameters
        recommended = {
            "category_weights": {
                "rain": 0.5,
                "thunder": 0.3,
                "white_noise": 0.5,
                "nature": 0.5,
                "water": 0.5,
                "other": 0.3,
            },
            "eq_preferences": {
                "low": 0,
                "mid-low": 0,
                "mid": 0,
                "high-mid": 0,
                "high": 0,
            },
            "volume_preferences": {"base_sounds": 0, "occasional_sounds": -3},
        }

        # Update with learned category weights for the sleep issue
        categories = trends.get("categories", {})
        for category, data in categories.items():
            issue_data = data.get("by_issue", {}).get(sleep_issue)
            if issue_data and "average_weight" in issue_data:
                recommended["category_weights"][category] = issue_data["average_weight"]

        # Find most effective sounds for the sleep issue
        effective_sounds = trends.get("effective_sounds_by_issue", {}).get(
            sleep_issue, {}
        )

        # Sort by average score
        sorted_sounds = [
            (sound, data["average_score"])
            for sound, data in effective_sounds.items()
            if "average_score" in data
        ]
        sorted_sounds.sort(key=lambda x: x[1], reverse=True)

        # Add top sounds
        recommended["recommended_sounds"] = [sound for sound, _ in sorted_sounds[:5]]

        logger.info(
            f"Generated recommended parameters for {sleep_issue} based on learning data"
        )
        return recommended
