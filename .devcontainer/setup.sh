#!/bin/bash
set -e

echo "🚀 Setting up Autotube development environment..."

# Update package list
echo "📦 Updating package list..."
sudo apt-get update

# Install FFmpeg (required for video generation)
echo "🎬 Installing FFmpeg..."
sudo apt-get install -y ffmpeg

# Install system dependencies for audio processing
echo "🔊 Installing audio processing libraries..."
sudo apt-get install -y \
    libsndfile1 \
    libportaudio2 \
    portaudio19-dev \
    libsdl2-dev \
    libsdl2-mixer-2.0-0

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install -r requirements.txt

# Install the package in development mode
echo "📦 Installing Autotube in development mode..."
pip install -e .

# Create necessary directories
echo "📁 Creating output directories..."
mkdir -p input_clips output_mixes output_videos

# Verify installations
echo ""
echo "✅ Setup complete! Verifying installations..."
echo ""

echo "Python version:"
python --version

echo ""
echo "FFmpeg version:"
ffmpeg -version | head -n 1

echo ""
echo "Key Python packages:"
pip list | grep -E "(pydub|librosa|click|pygame|tensorflow)" || echo "Some packages not found"

echo ""
echo "🎉 Autotube development environment is ready!"
echo ""
echo "To get started:"
echo "  - Run 'python -m project_name.cli status' to check system status"
echo "  - Run 'python -m project_name.cli gui' to launch the GUI"
echo "  - Run 'python -m project_name.cli --help' to see all commands"
echo ""
