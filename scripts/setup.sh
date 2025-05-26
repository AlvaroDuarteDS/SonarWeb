#!/bin/bash
echo "Setting up Voice Web Assistant..."

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create config directories
mkdir -p config logs temp

# Copy example config
cp .env.example .env

echo "Setup complete! Edit .env file with your OpenAI API key."
