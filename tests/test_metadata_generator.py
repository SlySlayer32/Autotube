"""Tests for the MetadataGenerator module."""

import pytest


class TestMetadataGenerator:
    """Test cases for MetadataGenerator class."""

    @pytest.fixture
    def generator(self):
        """Create a MetadataGenerator instance for testing."""
        from project_name.core.metadata_generator import MetadataGenerator

        return MetadataGenerator()

    def test_init(self, generator):
        """Test MetadataGenerator initialization."""
        assert generator is not None
        assert len(generator.TITLE_TEMPLATES) > 0
        assert len(generator.DESCRIPTION_TEMPLATES) > 0

    def test_generate_title_sleep(self, generator):
        """Test title generation for sleep videos."""
        title = generator.generate_title(
            sound_type="Rain",
            duration_hours=8,
            purpose="sleep",
        )
        assert title is not None
        assert len(title) > 0
        assert len(title) <= 100  # YouTube limit
        assert "Rain" in title or "rain" in title.lower()

    def test_generate_title_focus(self, generator):
        """Test title generation for focus videos."""
        title = generator.generate_title(
            sound_type="Ocean",
            duration_hours=2,
            purpose="focus",
        )
        assert title is not None
        assert len(title) <= 100

    def test_generate_title_relax(self, generator):
        """Test title generation for relax videos."""
        title = generator.generate_title(
            sound_type="Nature",
            duration_hours=4,
            purpose="relax",
        )
        assert title is not None
        assert len(title) <= 100

    def test_generate_title_custom_template(self, generator):
        """Test title generation with custom template."""
        custom = "{sound_type} - {duration}H Custom"
        title = generator.generate_title(
            sound_type="Rain",
            duration_hours=6,
            custom_template=custom,
        )
        assert title == "Rain - 6H Custom"

    def test_generate_description_sleep(self, generator):
        """Test description generation for sleep videos."""
        description = generator.generate_description(
            sound_type="Rain",
            duration_hours=8,
            purpose="sleep",
        )
        assert description is not None
        assert len(description) > 0
        assert len(description) <= 5000  # YouTube limit
        assert "sleep" in description.lower()

    def test_generate_description_with_additional_info(self, generator):
        """Test description generation with additional info."""
        additional = "Recorded in the Amazon rainforest."
        description = generator.generate_description(
            sound_type="Rain",
            duration_hours=8,
            purpose="sleep",
            additional_info=additional,
        )
        assert additional in description

    def test_generate_tags_sleep(self, generator):
        """Test tag generation for sleep videos."""
        tags = generator.generate_tags(
            sound_type="rain",
            purpose="sleep",
        )
        assert isinstance(tags, list)
        assert len(tags) > 0
        assert len(tags) <= 30
        assert "rain" in tags or "rainsounds" in tags
        assert "sleep" in tags or "sleepsounds" in tags

    def test_generate_tags_with_additional(self, generator):
        """Test tag generation with additional tags."""
        additional = ["custom1", "custom2"]
        tags = generator.generate_tags(
            sound_type="ocean",
            purpose="relax",
            additional_tags=additional,
        )
        assert "custom1" in tags
        assert "custom2" in tags

    def test_generate_tags_no_duplicates(self, generator):
        """Test that generated tags have no duplicates."""
        tags = generator.generate_tags(
            sound_type="rain",
            purpose="sleep",
            additional_tags=["rain", "sleep", "custom"],
        )
        # Check for duplicates (case-insensitive)
        lower_tags = [t.lower() for t in tags]
        assert len(lower_tags) == len(set(lower_tags))

    def test_generate_complete_metadata(self, generator):
        """Test complete metadata generation."""
        metadata = generator.generate_complete_metadata(
            sound_type="Rain",
            duration_hours=8,
            purpose="sleep",
        )
        assert "title" in metadata
        assert "description" in metadata
        assert "tags" in metadata
        assert "generated_at" in metadata

        assert len(metadata["title"]) <= 100
        assert len(metadata["description"]) <= 5000
        assert len(metadata["tags"]) <= 30

    def test_generate_scheduled_metadata(self, generator):
        """Test scheduled metadata generation."""
        from datetime import datetime

        publish_date = datetime(2024, 1, 15, 20, 0)
        metadata = generator.generate_scheduled_metadata(
            sound_type="Ocean",
            duration_hours=6,
            purpose="relax",
            publish_date=publish_date,
        )
        assert "scheduled_publish" in metadata
        assert "2024-01-15" in metadata["scheduled_publish"]

    def test_get_optimal_publish_time_sleep(self, generator):
        """Test optimal publish time for sleep content."""
        times = generator.get_optimal_publish_time(purpose="sleep")
        assert "weekday" in times
        assert "weekend" in times
        assert "best_days" in times
        assert "20:00" in times["weekday"]  # Evening for sleep

    def test_get_optimal_publish_time_focus(self, generator):
        """Test optimal publish time for focus content."""
        times = generator.get_optimal_publish_time(purpose="focus")
        assert "08:00" in times["weekday"]  # Morning for focus

    def test_get_optimal_publish_time_relax(self, generator):
        """Test optimal publish time for relax content."""
        times = generator.get_optimal_publish_time(purpose="relax")
        assert "18:00" in times["weekday"]  # Evening for relaxation


class TestMetadataGeneratorEdgeCases:
    """Test edge cases for MetadataGenerator."""

    @pytest.fixture
    def generator(self):
        """Create a MetadataGenerator instance."""
        from project_name.core.metadata_generator import MetadataGenerator

        return MetadataGenerator()

    def test_very_long_sound_type(self, generator):
        """Test with a very long sound type name."""
        long_name = "A" * 100
        title = generator.generate_title(
            sound_type=long_name,
            duration_hours=8,
        )
        assert len(title) <= 100

    def test_unknown_purpose(self, generator):
        """Test with an unknown purpose defaults gracefully."""
        title = generator.generate_title(
            sound_type="Rain",
            duration_hours=8,
            purpose="unknown_purpose",
        )
        # Should still generate something
        assert title is not None
        assert len(title) > 0

    def test_unknown_sound_type_tags(self, generator):
        """Test tags for unknown sound type."""
        tags = generator.generate_tags(
            sound_type="unknown_type",
            purpose="sleep",
        )
        # Should still include purpose tags and general tags
        assert len(tags) > 0
        assert any("sleep" in t.lower() for t in tags)

    def test_zero_duration(self, generator):
        """Test with zero duration."""
        metadata = generator.generate_complete_metadata(
            sound_type="Rain",
            duration_hours=0,
            purpose="sleep",
        )
        assert metadata["title"] is not None

    def test_large_duration(self, generator):
        """Test with large duration."""
        metadata = generator.generate_complete_metadata(
            sound_type="Rain",
            duration_hours=24,
            purpose="sleep",
        )
        assert "24" in metadata["title"]
