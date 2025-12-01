"""
Metadata Generator Module for Autotube.

This module provides functionality to generate optimized, templated
metadata (titles, descriptions, and tags) for sleep/relaxation videos.
"""

import logging
import random
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)


class MetadataGenerator:
    """
    Generate SEO-optimized metadata for sleep and relaxation videos.

    This class provides templated generation of titles, descriptions,
    and tags that are optimized for YouTube search and discovery.
    """

    # Default templates for different video types
    TITLE_TEMPLATES = {
        "sleep": [
            "{sound_type} Sounds for Deep Sleep - {duration} Hours",
            "{duration} Hours of {sound_type} for Sleeping",
            "Sleep Better with {sound_type} - {duration}H {quality} Sound",
            "{sound_type} White Noise for Sleep - {duration} Hours",
            "Relaxing {sound_type} Sounds - Fall Asleep Fast",
            "{duration} Hour {sound_type} | Sleep Sounds",
            "Deep Sleep {sound_type} - {duration} Hours of Relaxation",
            "{sound_type} for Sleep and Relaxation | {duration}H",
        ],
        "focus": [
            "{sound_type} for Focus and Concentration - {duration} Hours",
            "Study with {sound_type} - {duration}H Focus Music",
            "{duration} Hours {sound_type} for Work and Study",
            "Ambient {sound_type} for Productivity - {duration}H",
            "Focus Better with {sound_type} | {duration} Hours",
            "{sound_type} Sounds for Deep Work - {duration}H",
        ],
        "relax": [
            "Relaxing {sound_type} Sounds - {duration} Hours",
            "{duration} Hours of Calming {sound_type}",
            "Stress Relief {sound_type} - {duration}H Relaxation",
            "Peaceful {sound_type} for Meditation - {duration} Hours",
            "{sound_type} Ambient Sounds - {duration}H Peace",
            "Unwind with {sound_type} | {duration} Hours",
        ],
    }

    DESCRIPTION_TEMPLATES = {
        "sleep": """🌙 {sound_type} Sounds for Sleep | {duration} Hours

Drift off to peaceful sleep with this {duration}-hour recording of {sound_type_lower} sounds. Perfect for:
• Deep, restful sleep
• Blocking out distracting noises
• Creating a calming bedtime routine
• Baby sleep and nursery

{additional_info}

⏰ Duration: {duration} hours of uninterrupted {sound_type_lower}

🎧 Tips for best results:
- Set your device to airplane mode to avoid interruptions
- Use comfortable headphones or speakers
- Adjust volume to a comfortable level
- Make your room dark and cool

💤 Sleep Benefits:
{sound_type} sounds have been shown to help mask disruptive noises and create a consistent audio environment that promotes better sleep quality.

📌 Subscribe for more sleep sounds and relaxation content!

#sleep #sleepsounds #{sound_tag} #whitenoise #relax #meditation

---
{sound_type} Sounds for Deep Sleep - {duration} Hours
""",
        "focus": """🎯 {sound_type} for Focus | {duration} Hours

Enhance your concentration and productivity with this {duration}-hour recording of {sound_type_lower} sounds. Ideal for:
• Studying and homework
• Remote work and office focus
• Reading and writing
• Creative projects

{additional_info}

⏰ Duration: {duration} hours of consistent ambient sound

📚 Study Tips:
- Use the Pomodoro technique (25 min work, 5 min break)
- Find a comfortable workspace
- Stay hydrated
- Take regular breaks

🧠 Why it works:
Ambient sounds like {sound_type_lower} can help mask distracting noises and create a consistent audio backdrop that improves focus and cognitive performance.

📌 Subscribe for more focus and productivity sounds!

#focus #study #{sound_tag} #productivity #concentration #work

---
{sound_type} Sounds for Focus - {duration} Hours
""",
        "relax": """🧘 Relaxing {sound_type} | {duration} Hours

Unwind and de-stress with this {duration}-hour recording of peaceful {sound_type_lower} sounds. Perfect for:
• Meditation and mindfulness
• Yoga and stretching
• Stress relief
• Quiet time and reflection

{additional_info}

⏰ Duration: {duration} hours of calming ambience

🌿 Relaxation Tips:
- Find a comfortable position
- Close your eyes and focus on your breathing
- Let go of tension in your body
- Allow thoughts to come and go naturally

💆 Benefits of relaxation:
Regular relaxation practice can reduce stress, lower blood pressure, improve sleep quality, and enhance overall well-being.

📌 Subscribe for more relaxation and meditation sounds!

#relax #meditation #{sound_tag} #stressrelief #mindfulness #calm

---
Relaxing {sound_type} Sounds - {duration} Hours
""",
    }

    # Common tags for different sound types and purposes
    SOUND_TYPE_TAGS = {
        "rain": [
            "rain",
            "rainsounds",
            "rainfall",
            "rainstorm",
            "rainforest",
            "thunderstorm",
            "rainloop",
        ],
        "ocean": [
            "ocean",
            "oceansounds",
            "waves",
            "seasounds",
            "beach",
            "oceanwaves",
            "seawaves",
        ],
        "nature": [
            "nature",
            "naturesounds",
            "forest",
            "birds",
            "wildlife",
            "ambient",
            "outdoor",
        ],
        "white_noise": [
            "whitenoise",
            "pinknoise",
            "brownnoise",
            "noise",
            "static",
            "fan",
            "fansound",
        ],
        "ambient": [
            "ambient",
            "ambience",
            "atmospheric",
            "soundscape",
            "background",
            "mood",
        ],
    }

    PURPOSE_TAGS = {
        "sleep": [
            "sleep",
            "sleepsounds",
            "deepsleep",
            "sleeping",
            "insomnia",
            "babysleep",
            "sleepaid",
            "bedtime",
        ],
        "focus": [
            "focus",
            "study",
            "studying",
            "concentration",
            "productivity",
            "work",
            "studymusic",
            "focusmusic",
        ],
        "relax": [
            "relax",
            "relaxation",
            "calm",
            "peaceful",
            "meditation",
            "stressrelief",
            "zen",
            "mindfulness",
        ],
    }

    QUALITY_ADJECTIVES = [
        "HD",
        "High Quality",
        "Premium",
        "Crystal Clear",
        "Studio Quality",
        "Authentic",
        "Natural",
        "Pure",
    ]

    def __init__(self):
        """Initialize the MetadataGenerator."""
        logger.info("MetadataGenerator initialized")

    def generate_title(
        self,
        sound_type: str,
        duration_hours: int = 8,
        purpose: str = "sleep",
        custom_template: str = None,
    ) -> str:
        """
        Generate an SEO-optimized video title.

        Args:
            sound_type: Type of sound (e.g., "Rain", "Ocean", "Nature").
            duration_hours: Duration of the video in hours.
            purpose: Purpose of the video ("sleep", "focus", "relax").
            custom_template: Optional custom title template.

        Returns:
            Generated title string.
        """
        if custom_template:
            template = custom_template
        else:
            templates = self.TITLE_TEMPLATES.get(
                purpose, self.TITLE_TEMPLATES["sleep"]
            )
            template = random.choice(templates)

        quality = random.choice(self.QUALITY_ADJECTIVES)

        title = template.format(
            sound_type=sound_type.title(),
            duration=duration_hours,
            quality=quality,
        )

        # Ensure title doesn't exceed YouTube's 100 character limit
        if len(title) > 100:
            title = title[:97] + "..."

        logger.info(f"Generated title: {title}")
        return title

    def generate_description(
        self,
        sound_type: str,
        duration_hours: int = 8,
        purpose: str = "sleep",
        additional_info: str = "",
        custom_template: str = None,
    ) -> str:
        """
        Generate an SEO-optimized video description.

        Args:
            sound_type: Type of sound (e.g., "Rain", "Ocean", "Nature").
            duration_hours: Duration of the video in hours.
            purpose: Purpose of the video ("sleep", "focus", "relax").
            additional_info: Additional information to include.
            custom_template: Optional custom description template.

        Returns:
            Generated description string.
        """
        if custom_template:
            template = custom_template
        else:
            template = self.DESCRIPTION_TEMPLATES.get(
                purpose, self.DESCRIPTION_TEMPLATES["sleep"]
            )

        # Create sound tag from sound type
        sound_tag = sound_type.lower().replace(" ", "")

        description = template.format(
            sound_type=sound_type.title(),
            sound_type_lower=sound_type.lower(),
            duration=duration_hours,
            additional_info=additional_info,
            sound_tag=sound_tag,
        )

        # Ensure description doesn't exceed YouTube's 5000 character limit
        if len(description) > 5000:
            description = description[:4997] + "..."

        logger.info(f"Generated description ({len(description)} chars)")
        return description

    def generate_tags(
        self,
        sound_type: str,
        purpose: str = "sleep",
        additional_tags: list = None,
        max_tags: int = 30,
    ) -> list:
        """
        Generate SEO-optimized tags for the video.

        Args:
            sound_type: Type of sound (e.g., "rain", "ocean", "nature").
            purpose: Purpose of the video ("sleep", "focus", "relax").
            additional_tags: Additional custom tags to include.
            max_tags: Maximum number of tags to generate.

        Returns:
            List of tags.
        """
        tags = []

        # Add sound type specific tags
        sound_key = sound_type.lower().replace(" ", "_")
        if sound_key in self.SOUND_TYPE_TAGS:
            tags.extend(self.SOUND_TYPE_TAGS[sound_key])
        else:
            # Generic tags for unknown sound types
            tags.append(sound_type.lower().replace(" ", ""))

        # Add purpose-specific tags
        if purpose in self.PURPOSE_TAGS:
            tags.extend(self.PURPOSE_TAGS[purpose])

        # Add general video tags
        general_tags = [
            "asmr",
            "relaxingsounds",
            "ambience",
            "soundscape",
            "blackscreen",
            "8hours",
            "10hours",
            "allnight",
        ]
        tags.extend(general_tags)

        # Add additional custom tags
        if additional_tags:
            tags.extend(additional_tags)

        # Remove duplicates while preserving order
        seen = set()
        unique_tags = []
        for tag in tags:
            tag_lower = tag.lower()
            if tag_lower not in seen:
                seen.add(tag_lower)
                unique_tags.append(tag)

        # Limit to max_tags
        result = unique_tags[:max_tags]
        logger.info(f"Generated {len(result)} tags")
        return result

    def generate_complete_metadata(
        self,
        sound_type: str,
        duration_hours: int = 8,
        purpose: str = "sleep",
        additional_info: str = "",
        additional_tags: list = None,
    ) -> dict:
        """
        Generate complete metadata for a video.

        Args:
            sound_type: Type of sound (e.g., "Rain", "Ocean", "Nature").
            duration_hours: Duration of the video in hours.
            purpose: Purpose of the video ("sleep", "focus", "relax").
            additional_info: Additional information for description.
            additional_tags: Additional custom tags.

        Returns:
            Dictionary containing title, description, and tags.
        """
        metadata = {
            "title": self.generate_title(sound_type, duration_hours, purpose),
            "description": self.generate_description(
                sound_type, duration_hours, purpose, additional_info
            ),
            "tags": self.generate_tags(sound_type, purpose, additional_tags),
            "generated_at": datetime.now().isoformat(),
        }

        logger.info(f"Generated complete metadata for {sound_type} {purpose} video")
        return metadata

    def generate_scheduled_metadata(
        self,
        sound_type: str,
        duration_hours: int = 8,
        purpose: str = "sleep",
        publish_date: Optional[datetime] = None,
    ) -> dict:
        """
        Generate metadata with scheduling information.

        Args:
            sound_type: Type of sound (e.g., "Rain", "Ocean", "Nature").
            duration_hours: Duration of the video in hours.
            purpose: Purpose of the video ("sleep", "focus", "relax").
            publish_date: Scheduled publish date/time.

        Returns:
            Dictionary containing metadata with scheduling info.
        """
        metadata = self.generate_complete_metadata(
            sound_type, duration_hours, purpose
        )

        if publish_date:
            metadata["scheduled_publish"] = publish_date.isoformat()

            # Add time-specific info to description
            day_name = publish_date.strftime("%A")
            metadata["description"] = (
                f"🗓️ New video every {day_name}!\n\n" + metadata["description"]
            )

        return metadata

    def get_optimal_publish_time(
        self,
        purpose: str = "sleep",
        timezone: str = "UTC",
    ) -> dict:
        """
        Get suggested optimal publish times for different video types.

        Args:
            purpose: Purpose of the video ("sleep", "focus", "relax").
            timezone: Target timezone for publish time.

        Returns:
            Dictionary with suggested publish times.
        """
        # Research-based optimal times for different content types
        optimal_times = {
            "sleep": {
                "weekday": "20:00",  # 8 PM - People preparing for bed
                "weekend": "21:00",  # 9 PM - Later bedtime on weekends
                "best_days": ["Sunday", "Thursday"],
            },
            "focus": {
                "weekday": "08:00",  # 8 AM - Start of work/study day
                "weekend": "10:00",  # 10 AM - Later start on weekends
                "best_days": ["Monday", "Tuesday", "Wednesday"],
            },
            "relax": {
                "weekday": "18:00",  # 6 PM - After work
                "weekend": "15:00",  # 3 PM - Afternoon relaxation
                "best_days": ["Friday", "Saturday", "Sunday"],
            },
        }

        times = optimal_times.get(purpose, optimal_times["sleep"])
        times["timezone"] = timezone
        times["purpose"] = purpose

        logger.info(f"Optimal publish times for {purpose}: {times}")
        return times
