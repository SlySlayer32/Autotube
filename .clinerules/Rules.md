# Cline Rules for Ambient Audio Processing Project

project_context:
  name: "Ambient Audio Processing Tool"
  purpose: "Tool for processing and mixing ambient audio for sleep and relaxation"
  target_users: "End users seeking personalized ambient soundscapes"
  
architecture_principles:

- "Use existing proven audio libraries (librosa, essentia, pedalboard) over custom implementations"
- "Maintain clear separation between core logic, GUI, and API integrations"
- "Implement comprehensive error handling and logging"
- "Design for extensibility - new audio sources and effects should be easy to add"
- "Prioritize audio quality and processing efficiency"

code_standards:
  python_version: "3.9+"
  style_guide: "PEP 8 with black formatting"
  type_hints: "Required for all public methods and complex functions"
  docstrings: "Google style docstrings for all classes and public methods"
  testing: "pytest with minimum 80% coverage for core functionality"
  
dependencies:
  core_audio: ["librosa", "soundfile", "numpy", "scipy"]
  advanced_processing: ["essentia-tensorflow", "pedalboard", "openl3"]
  ml_classification: ["tensorflow", "tensorflow-hub", "scikit-learn"]
  gui: ["tkinter", "matplotlib", "plotly"]
  api: ["requests", "python-dotenv"]
  development: ["pytest", "black", "mypy", "poetry"]

project_structure_rules:

- "Keep audio processing logic in core/ directory"
- "GUI components should be modular and testable"
- "API integrations should handle rate limiting and errors gracefully"
- "Utils should contain only pure functions without side effects"
- "All file I/O should include proper error handling"
- "Audio files should be validated before processing"

performance_requirements:

- "Audio processing should handle files up to 1 hour in length"
- "Real-time preview should have < 100ms latency"
- "Memory usage should not exceed 2GB for typical operations"
- "Support concurrent processing of multiple files"

quality_gates:

- "All audio outputs must maintain 44.1kHz/16-bit minimum quality"
- "No audio artifacts or clipping in processed files"
- "Graceful degradation when external APIs are unavailable"
- "User-friendly error messages for common issues"

security_considerations:

- "API keys must be stored in environment variables"
- "Validate all user inputs, especially file paths"
- "Sanitize filenames to prevent directory traversal"
- "Rate limit API calls to external services"

refactoring_priorities:
  high:
    - "Complete SoundProcessor._classify_by_rules implementation"
    - "Implement functional SoundToolGUI class"
    - "Add audio preview functionality"
    - "Integrate advanced audio analysis (YAMNet, OpenL3)"
  medium:
    - "Add binaural beats generation"
    - "Implement personalized mix recommendations"
    - "Add batch processing capabilities"
    - "Create comprehensive test suite"
  low:
    - "Add more audio effects options"
    - "Implement user preference persistence"
    - "Add export format options"
    - "Create CLI interface improvements"

common_patterns:
  error_handling: |
    try:
        # audio processing code
        pass
    except (librosa.LibrosaError, soundfile.SoundFileError) as e:
        logger.error(f"Audio processing error: {e}")
        raise AudioProcessingError(f"Failed to process audio: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise

  logging_format: |
    import logging
    logger = logging.getLogger(__name__)
    logger.info("Processing started for file: %s", filename)

  type_hints_example: |
    from typing import List, Dict, Optional, Union
    from pathlib import Path

    def process_audio(
        input_path: Union[str, Path],
        output_path: Union[str, Path],
        effects: Optional[List[str]] = None
    ) -> Dict[str, Any]:

file_organization:

- "Group related functionality in modules"
- "Keep configuration separate from logic"
- "Use pathlib.Path for all file operations"
- "Maintain consistent naming conventions"
- "Include __init__.py files with proper imports"

when_refactoring:
  always_check:
    - "Does this maintain backward compatibility?"
    - "Are there sufficient tests for the changes?"
    - "Is error handling comprehensive?"
    - "Are type hints accurate and helpful?"
    - "Does this follow the established patterns?"
  
  before_suggesting_changes:
    - "Review the current TODO list in README.md"
    - "Consider impact on existing functionality"
    - "Ensure changes align with project goals"
    - "Check if external dependencies are justified"
    - "Verify that changes improve user experience"

integration_guidelines:
  freesound_api:
    - "Implement proper rate limiting (5 requests/second max)"
    - "Cache responses when appropriate"
    - "Handle authentication errors gracefully"
    - "Provide fallback when API is unavailable"
  
  audio_libraries:
    - "Use librosa for basic audio analysis"
    - "Use essentia for advanced music analysis"
    - "Use pedalboard for real-time effects"
    - "Use soundfile for I/O operations"

user_experience_priorities:

- "Provide clear progress indicators for long operations"
- "Show meaningful error messages with suggested solutions"
- "Allow users to preview before processing"
- "Support drag-and-drop file operations"
- "Remember user preferences between sessions"
