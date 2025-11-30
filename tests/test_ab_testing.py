"""Tests for AB testing functionality."""

import time
from pathlib import Path
from typing import Dict

import pytest

from project_name.core.ab_testing import ABTest, MixLearner
from project_name.core.user_profile import UserProfile


@pytest.mark.unit
class TestABTest:
    def test_init(self):
        """Test ABTest initialization."""
        test = ABTest()
        assert test.test_id.startswith("abtest_")
        assert test.creation_time <= time.time()
        assert test.test_parameter is None
        assert test.parameter_values == {}
        assert test.variant_a_params == {}
        assert test.variant_b_params == {}
        assert test.result is None
        assert test.feedback == {}

    def test_setup_test_basic_parameter(self):
        """Test setting up test with a basic parameter."""
        test = ABTest()
        test.setup_test("volume", -3, 0, {"base": "params"})

        assert test.test_parameter == "volume"
        assert test.parameter_values == {"A": -3, "B": 0}
        assert test.variant_a_params == {"base": "params", "volume": -3}
        assert test.variant_b_params == {"base": "params", "volume": 0}

    def test_setup_test_category_weight(self):
        """Test setting up test with category weight parameter."""
        test = ABTest()
        test.setup_test("category_weights.rain", 0.7, 0.4, {"other_param": "value"})

        assert test.test_parameter == "category_weights.rain"
        assert test.variant_a_params["category_weights"]["rain"] == 0.7
        assert test.variant_b_params["category_weights"]["rain"] == 0.4

    def test_record_result(self):
        """Test recording test results."""
        test = ABTest()
        feedback = {"quality": "good", "comments": "Preferred the louder version"}
        test.record_result("A", feedback)

        assert test.result == "A"
        assert test.feedback == feedback

    def test_get_learning_delta_numeric(self):
        """Test learning delta calculation for numeric parameters."""
        test = ABTest()
        test.setup_test("volume", -3, 0)
        test.record_result("A")

        param, delta = test.get_learning_delta()
        assert param == "volume"
        assert delta < 0  # Should move toward -3 (variant A)

    def test_save_and_load(self, temp_dir: Path):
        """Test saving and loading AB test data."""
        test = ABTest("test_123")
        test.setup_test("volume", -3, 0)
        test.record_result("A")

        # Save test
        save_path = test.save(temp_dir)
        assert save_path.exists()

        # Load test (convert Path to str)
        loaded_test = ABTest.load(str(save_path))
        assert loaded_test.test_id == test.test_id
        assert loaded_test.test_parameter == test.test_parameter
        assert loaded_test.parameter_values == test.parameter_values
        assert loaded_test.result == test.result


@pytest.mark.unit
class TestMixLearner:
    def test_init(self):
        """Test MixLearner initialization."""
        learner = MixLearner()
        assert learner.profiles == {}
        assert learner.ab_tests == []
        assert isinstance(learner.learning_rate, float)
        assert len(learner.test_parameters) > 0

    def test_create_ab_test(self, mock_user_profile: Dict):
        """Test creating a new AB test."""
        learner = MixLearner()
        # Create profile correctly
        profile = UserProfile(
            name=mock_user_profile["name"], sleep_issue=mock_user_profile["sleep_issue"]
        )
        profile.category_weights = mock_user_profile["category_weights"]
        profile.eq_preferences = mock_user_profile["eq_preferences"]
        profile.volume_preferences = mock_user_profile["volume_preferences"]
        learner.profiles[profile.name] = profile

        test = learner.create_ab_test(profile.name)
        assert test.test_id.startswith("abtest_")
        assert test.test_parameter in learner.test_parameters
        assert test in learner.ab_tests

    def test_record_ab_test_result(self, mock_user_profile: Dict):
        """Test recording AB test results and profile updates."""
        learner = MixLearner()
        # Create profile correctly
        profile = UserProfile(
            name=mock_user_profile["name"], sleep_issue=mock_user_profile["sleep_issue"]
        )
        profile.category_weights = mock_user_profile["category_weights"]
        profile.eq_preferences = mock_user_profile["eq_preferences"]
        profile.volume_preferences = mock_user_profile["volume_preferences"]
        learner.profiles[profile.name] = profile

        test = learner.create_ab_test(profile.name)
        original_value = (
            profile.category_weights["rain"]
            if test.test_parameter.startswith("category_weights")
            else profile.volume_preferences["base_sounds"]
        )

        learner.record_ab_test_result(test.test_id, "A")
        assert test.result == "A"

        # Verify profile was updated
        if test.test_parameter.startswith("category_weights"):
            assert profile.category_weights["rain"] != original_value

    def test_optimize_mix_parameters(self, mock_user_profile: Dict):
        """Test mix parameter optimization based on user profile."""
        learner = MixLearner()
        # Create profile correctly
        profile = UserProfile(
            name=mock_user_profile["name"], sleep_issue=mock_user_profile["sleep_issue"]
        )
        profile.category_weights = mock_user_profile["category_weights"]
        profile.eq_preferences = mock_user_profile["eq_preferences"]
        profile.volume_preferences = mock_user_profile["volume_preferences"]
        learner.profiles[profile.name] = profile

        optimized = learner.optimize_mix_parameters(profile.name)
        assert "category_weights" in optimized
        assert optimized["category_weights"] == profile.category_weights
        assert "eq_preferences" in optimized
        assert optimized["eq_preferences"] == profile.eq_preferences
        assert "volume_preferences" in optimized
        assert optimized["volume_preferences"] == profile.volume_preferences

    @pytest.mark.slow
    def test_analyze_learning_trends(self, mock_user_profile: Dict):
        """Test analysis of learning trends across users and tests."""
        learner = MixLearner()
        # Create profile correctly
        profile = UserProfile(
            name=mock_user_profile["name"], sleep_issue=mock_user_profile["sleep_issue"]
        )
        profile.category_weights = mock_user_profile["category_weights"]
        profile.eq_preferences = mock_user_profile["eq_preferences"]
        profile.volume_preferences = mock_user_profile["volume_preferences"]
        learner.profiles[profile.name] = profile

        # Create and complete several tests
        for _ in range(3):
            test = learner.create_ab_test(profile.name)
            learner.record_ab_test_result(test.test_id, "A")

        trends = learner.analyze_learning_trends()
        assert "parameters" in trends
        assert "categories" in trends
        assert "sleep_issues" in trends
        assert profile.sleep_issue in trends["sleep_issues"]
