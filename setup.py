from setuptools import find_packages, setup

setup(
    name="project_name",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pydub>=0.25.1",
        "librosa>=0.10.0",
        "scikit-learn>=1.2.0",
        "numpy>=1.21.0",
        "matplotlib>=3.5.0",
        "pillow>=9.0.0",
        "requests>=2.28.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.3.1",
            "pytest-cov>=4.1.0",
            "watchdog>=3.0.0",
            "black>=24.0.0",
            "mypy>=1.5.0",
        ],
        "test": [
            "pytest>=7.3.1",
            "pytest-cov>=4.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "sonicsleep=project_name.cli:main",
        ],
    },
    python_requires=">=3.10",
)
