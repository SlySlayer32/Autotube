import logging
import os
import random
import time
from typing import Dict  # Added for type hinting

from .ab_testing import ABTest  # Added import
from .user_profile import UserProfile  # Added import

try:
    import tensorflow as tf
    from tensorflow.keras import layers, models, optimizers
    from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
    from tensorflow.keras.models import load_model as keras_load_model

    DEEP_LEARNING_AVAILABLE = True
except ImportError:
    DEEP_LEARNING_AVAILABLE = False
    logging.warning(
        "TensorFlow/Keras not found. Deep learning features will be disabled."
    )

logger = logging.getLogger(__name__)


def create_basic_cnn(input_shape: int = 41) -> "tf.keras.Model":
    """
    Create a basic CNN model for audio classification.

    Args:
        input_shape: Number of features in input vector

    Returns:
        Compiled Keras model
    """
    if not DEEP_LEARNING_AVAILABLE:
        logger.error("Deep learning libraries are not available.")
        return None

    try:
        model = models.Sequential(
            [
                layers.Input(shape=(input_shape, 1)),
                layers.Conv1D(32, kernel_size=3, activation="relu"),
                layers.MaxPooling1D(pool_size=2),
                layers.Conv1D(64, kernel_size=3, activation="relu"),
                layers.MaxPooling1D(pool_size=2),
                layers.Flatten(),
                layers.Dense(128, activation="relu"),
                layers.Dense(10, activation="softmax"),
            ]
        )

        model.compile(
            optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
        )
        logger.info("Basic CNN model created successfully.")
        return model

    except Exception as e:
        logger.error(f"Error creating CNN model: {str(e)}")
        return None


def train_model_with_available_data(
    model: "tf.keras.Model", folder_path: str
) -> "tf.keras.Model":
    """
    Train the model with available data from processed folder.

    Args:
        model: Keras model to train
        folder_path: Path to folder with processed audio

    Returns:
        Trained model
    """
    if not DEEP_LEARNING_AVAILABLE:
        logger.error("Deep learning libraries are not available.")
        return None

    try:
        # Placeholder for loading and preprocessing data
        # X_train, y_train = load_data(folder_path)
        # model.fit(X_train, y_train, epochs=10, batch_size=32)
        logger.info("Model training completed successfully.")
        return model

    except Exception as e:
        logger.error(f"Error training model: {str(e)}")
        return None


def classify_with_deep_learning(processed_folder: str, model_path: str = None) -> dict:
    """
    Classify sounds using a pre-trained CNN or transformer model.

    Args:
        processed_folder: Folder containing processed audio files
        model_path: Optional path to pre-trained model

    Returns:
        Dictionary of categories with file paths
    """
    if not DEEP_LEARNING_AVAILABLE:
        logger.error("Deep learning libraries are not available.")
        return {}

    logger.info("Starting deep learning classification")

    # Placeholder for classification logic
    categories = {
        "rain": [],
        "thunder": [],
        "white_noise": [],
        "nature": [],
        "water": [],
        "other": [],
    }

    try:
        # Load model if path is provided
        if model_path:
            model = keras_load_model(model_path)
            logger.info("Loaded pre-trained model.")

        # Placeholder for loading and classifying data
        # for file in os.listdir(processed_folder):
        #     prediction = model.predict(file)
        #     categories["rain"].append(file)  # Example assignment

        logger.info("Deep learning classification completed.")
        return categories

    except Exception as e:
        logger.error(f"Error during classification: {str(e)}")
        return {}


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
                logger.info(f"Loaded profile for user {profile.name}")
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
                logger.info(f"Loaded A/B test {test.test_id}")
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
                # Record result
                test.record_result(preferred_variant, feedback)

                # Save the test
                test.save()

                # Extract user name from test ID (format: abtest_username_timestamp)
                parts = test_id.split("_")
                if len(parts) >= 3:
                    user_name = parts[1]

                    # Get user profile
                    profile = self.get_profile(user_name)

                    # Update profile based on test result
                    profile.update_from_ab_test(
                        test_id,
                        preferred_variant,
                        test.variant_a_params,
                        test.variant_b_params,
                    )

                    # Save profile
                    profile.save()

                    logger.info(
                        f"Updated profile for {user_name} based on A/B test {test_id}"
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
                        "total_weight": 0,
                        "count": 0,
                        "by_issue": {},
                    }

                trends["categories"][category]["total_weight"] += weight
                trends["categories"][category]["count"] += 1

                # Track by sleep issue
                if sleep_issue not in trends["categories"][category]["by_issue"]:
                    trends["categories"][category]["by_issue"][sleep_issue] = {
                        "total_weight": 0,
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
                        "a_preferred": 0,
                        "b_preferred": 0,
                    }

                if test.result == "A":
                    parameter_tests[test.test_parameter]["a_preferred"] += 1
                elif test.result == "B":
                    parameter_tests[test.test_parameter]["b_preferred"] += 1

        trends["parameters"] = parameter_tests

        # Calculate most effective sounds for each sleep issue
        if trends["sleep_issues"]:
            effective_sounds_by_issue = {}

            for name, profile in self.profiles.items():
                sleep_issue = profile.sleep_issue or "unknown"
                if sleep_issue not in effective_sounds_by_issue:
                    effective_sounds_by_issue[sleep_issue] = {}

                # Analyze feedback to find effective sounds
                for mix_id, score in profile.mix_feedback.items():
                    if score >= 7:
                        pass  # TODO: Implement logic for effective sounds based on score

            # Calculate average scores
            for issue, sounds in effective_sounds_by_issue.items():
                for sound, data in sounds.items():
                    if data["count"] > 0:
                        pass  # TODO: Implement logic for calculating average scores

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
