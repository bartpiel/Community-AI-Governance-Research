#!/bin/bash

# Setup script for Nonprofit Foundation Analysis
# This script creates a virtual environment and installs dependencies

echo "🔧 Setting up Nonprofit Foundation Analysis environment..."

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3 and try again."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment."
        echo "Make sure python3-venv is installed: sudo apt install python3-venv"
        exit 1
    fi
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Setup completed successfully!"
    echo ""
    echo "To run the analysis:"
    echo "1. Activate the virtual environment: source venv/bin/activate"
    echo "2. Run the full analysis: python3 run_full_analysis.py"
    echo ""
    echo "Or run individual collectors:"
    echo "   python3 collectors/apache_foundation_collector.py"
    echo "   python3 collectors/eclipse_foundation_collector.py"
    echo "   python3 collectors/linux_foundation_collector.py"
    echo "   python3 collectors/mozilla_foundation_collector.py"
    echo "   python3 collectors/osi_ecosystem_collector.py"
    echo "   python3 collectors/fsf_ecosystem_collector.py"
else
    echo "❌ Failed to install dependencies."
    exit 1
fi