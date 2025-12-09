from setuptools import find_packages, setup

setup(
    name="project_name",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pydub>=0.25.1",
        "librosa>=0.10.0",
        "scikit-learn>=1.2.0",
        "numpy>=1.21.0,<1.25.0",
        "matplotlib>=3.5.0",
        "pillow>=10.0.0",
        "requests>=2.28.0",
        "python-dotenv>=1.0.0",
        "soundfile>=0.12.1",
        "tensorflow>=2.10.0,<2.16.0",
        "tensorflow-hub>=0.14.0,<0.16.0",
        "openl3>=0.4.2",
        "click>=8.0.0",
        "google-api-python-client>=2.0.0",
        "google-auth-httplib2>=0.1.0",
        "google-auth-oauthlib>=1.0.0",
        "pygame>=2.5.0",
        "scipy>=1.10.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.3.1",
            "pytest-cov>=4.0.0",
            "watchdog>=2.3.0",
            "ruff>=0.1.0",
            "mypy>=1.5.0",
        ],
        "test": [
            "pytest>=7.3.1",
            "pytest-cov>=4.0.0",
        ],
        "build": [
            "pyinstaller>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "autotube=project_name.cli:main",
        ],
    },
    python_requires=">=3.11.0,<3.12.0",
)
