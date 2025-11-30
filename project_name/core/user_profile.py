import json
import logging
import os
import time
from pathlib import Path  # Added missing import
from typing import Dict

logger = logging.getLogger(__name__)


class UserProfile:
    """
    Class to store user preferences and sleep issue profiles
    to enable personalized mix creation.
    """

    def __init__(self, name: str = "default", sleep_issue: str = None):
        """
        Initialize a user profile.

        Args:
            name: Name of the profile
            sleep_issue: Type of sleep issue (insomnia, anxiety, etc.)
        """
        self.name = name
        self.sleep_issue = sleep_issue
        self.creation_date = time.time()
        self.last_updated = time.time()

        # Default weights for sound categories based on sleep issue
        if sleep_issue == "insomnia":
            self.category_weights = {
                "rain": 0.7,
                "thunder": 0.2,
                "white_noise": 0.8,
                "nature": 0.5,
                "water": 0.6,
                "other": 0.3,
            }
        elif sleep_issue == "anxiety":
            self.category_weights = {
                "rain": 0.8,
                "thunder": 0.1,
                "white_noise": 0.5,
                "nature": 0.7,
                "water": 0.9,
                "other": 0.4,
            }
        else:  # Default/balanced profile
            self.category_weights = {
                "rain": 0.5,
                "thunder": 0.3,
                "white_noise": 0.5,
                "nature": 0.5,
                "water": 0.5,
                "other": 0.3,
            }

        # Sound preferences
        self.preferred_sounds = []  # List of preferred sound file paths
        self.avoided_sounds = []  # List of sounds to avoid

        # Mix preferences
        self.preferred_duration = 60  # in minutes
        self.volume_preferences = {
            "base_sounds": 0,  # dB adjustment
            "occasional_sounds": -3,  # dB adjustment
        }

        # EQ preferences (boost/cut in dB for frequency bands)
        self.eq_preferences = {
            "low": 0,  # 20-200Hz
            "mid-low": 0,  # 200-800Hz
            "mid": 0,  # 800-2000Hz
            "high-mid": 0,  # 2000-5000Hz
            "high": 0,  # 5000-20000Hz
        }

        # Feedback history
        self.mix_feedback = {}  # Mix ID to feedback score (1-10)

        # A/B test results
        self.ab_test_results = {}  # Test ID to preferred variant (A or B)

    def update_from_feedback(
        self, mix_id: str, feedback_score: int, mix_params: Dict
    ) -> None:
        """
        Update profile based on mix feedback.

        Args:
            mix_id: ID of the mix
            feedback_score: User feedback score (1-10)
            mix_params: Parameters used to create the mix
        """
        # Store feedback
        self.mix_feedback[mix_id] = feedback_score
        self.last_updated = time.time()

        # Update category weights based on feedback
        if feedback_score >= 7:  # Good feedback
            # Slightly increase weights for categories used in the mix
            for category, weight in mix_params.get("category_weights", {}).items():
                if category in self.category_weights:
                    # Increase by 10% of the difference to 1.0, capped at 0.95
                    self.category_weights[category] = min(
                        0.95,
                        self.category_weights[category]
                        + (1.0 - self.category_weights[category]) * 0.1,
                    )

            # Add any preferred sounds
            preferred_sounds = mix_params.get("primary_sounds", [])
            for sound in preferred_sounds:
                if sound not in self.preferred_sounds:
                    self.preferred_sounds.append(sound)
                    logger.info(f"Added {sound} to preferred sounds for {self.name}")

        elif feedback_score <= 4:  # Negative feedback
            # Slightly decrease weights for categories used in the mix
            for category, weight in mix_params.get("category_weights", {}).items():
                if category in self.category_weights and weight > 0.3:
                    # Decrease by 10%, but keep above 0.1
                    self.category_weights[category] = max(
                        0.1,
                        self.category_weights[category]
                        - self.category_weights[category] * 0.1,
                    )

            # Add to avoided sounds
            avoided_sounds = mix_params.get("primary_sounds", [])
            for sound in avoided_sounds:
                if sound not in self.avoided_sounds:
                    self.avoided_sounds.append(sound)
                    logger.info(f"Added {sound} to avoided sounds for {self.name}")

        logger.info(
            f"Updated profile for {self.name} based on feedback (score: {feedback_score})"
        )

    def update_from_ab_test(
        self,
        test_id: str,
        preferred_variant: str,
        variant_a_params: Dict,
        variant_b_params: Dict,
    ) -> None:
        """
        Update profile based on A/B test results.

        Args:
            test_id: ID of the A/B test
            preferred_variant: User's preferred variant ('A' or 'B')
            variant_a_params: Parameters used for variant A
            variant_b_params: Parameters used for variant B
        """
        # Store result
        self.ab_test_results[test_id] = preferred_variant
        self.last_updated = time.time()

        # Get the preferred and non-preferred parameters
        if preferred_variant == "A":
            preferred_params = variant_a_params
            non_preferred_params = variant_b_params
        else:
            preferred_params = variant_b_params
            non_preferred_params = variant_a_params

        # Update preferences based on the test
        if "primary_category" in preferred_params:
            # Increase weight for preferred category
            category = preferred_params["primary_category"]
            if category in self.category_weights:
                self.category_weights[category] = min(
                    1.0, self.category_weights[category] + 0.1
                )

        if "eq_settings" in preferred_params:
            # Adjust EQ preferences
            for band, value in preferred_params["eq_settings"].items():
                if band in self.eq_preferences:
                    # Move 30% of the way toward the preferred value
                    current = self.eq_preferences[band]
                    self.eq_preferences[band] = current + (value - current) * 0.3

        if "volume_levels" in preferred_params:
            # Adjust volume preferences
            for key, value in preferred_params["volume_levels"].items():
                if key in self.volume_preferences:
                    # Move 30% of the way toward the preferred value
                    current = self.volume_preferences[key]
                    self.volume_preferences[key] = current + (value - current) * 0.3

        logger.info(
            f"Updated profile for {self.name} based on A/B test (preferred: variant {preferred_variant})"
        )

    def save(
        self, folder_path: str = "user_profiles"
    ) -> Path:  # Changed return type hint to Path
        """
        Save the user profile to a file.

        Args:
            folder_path: Folder to save profile in

        Returns:
            Path to saved profile file
        """
        os.makedirs(folder_path, exist_ok=True)

        # Create filename
        filename = f"{self.name.lower().replace(' ', '_')}_profile.json"
        file_path = os.path.join(folder_path, filename)

        # Convert to dict for serialization
        profile_data = {
            "name": self.name,
            "sleep_issue": self.sleep_issue,
            "creation_date": self.creation_date,
            "last_updated": self.last_updated,
            "category_weights": self.category_weights,
            "preferred_sounds": self.preferred_sounds,
            "avoided_sounds": self.avoided_sounds,
            "preferred_duration": self.preferred_duration,
            "volume_preferences": self.volume_preferences,
            "eq_preferences": self.eq_preferences,
            "mix_feedback": self.mix_feedback,
            "ab_test_results": self.ab_test_results,
        }

        # Save to file
        with open(file_path, "w") as f:
            json.dump(profile_data, f, indent=2)

        logger.info(f"Saved user profile to {file_path}")
        return Path(file_path)  # Return Path object

    @classmethod
    def load(cls, file_path: str) -> "UserProfile":
        """
        Load a user profile from file.

        Args:
            file_path: Path to profile file

        Returns:
            Loaded UserProfile object
        """
        try:
            with open(file_path, "r") as f:
                profile_data = json.load(f)

            # Create new profile instance
            profile = cls(name=profile_data.get("name", "default"))

            # Load attributes
            profile.sleep_issue = profile_data.get("sleep_issue")
            profile.creation_date = profile_data.get("creation_date", time.time())
            profile.last_updated = profile_data.get("last_updated", time.time())
            profile.category_weights = profile_data.get(
                "category_weights", profile.category_weights
            )
            profile.preferred_sounds = profile_data.get("preferred_sounds", [])
            profile.avoided_sounds = profile_data.get("avoided_sounds", [])
            profile.preferred_duration = profile_data.get("preferred_duration", 60)
            profile.volume_preferences = profile_data.get(
                "volume_preferences", profile.volume_preferences
            )
            profile.eq_preferences = profile_data.get(
                "eq_preferences", profile.eq_preferences
            )
            profile.mix_feedback = profile_data.get("mix_feedback", {})
            profile.ab_test_results = profile_data.get("ab_test_results", {})

            logger.info(f"Loaded user profile from {file_path}")
            return profile

        except Exception as e:
            logger.error(f"Error loading profile from {file_path}: {str(e)}")
            # Return a default profile
            return cls(name="default")
