# Sonar Web

A powerful voice-controlled web browser assistant that allows you to navigate the web hands-free using natural voice commands. Built with Python, Selenium, and OpenAI's GPT-4 Vision API.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

## Features

- **Voice Control**: Navigate the web entirely through voice commands
- **Visual Understanding**: Uses GPT-4 Vision to understand and describe web pages
- **Fast Response**: Edge-TTS provides near-instant voice feedback (<1 second)
- **Smart Caching**: Intelligent caching system for instant repeated queries
- **Auto Cookie Handling**: Automatically accepts cookie popups
- **Full Page Screenshots**: Captures entire web pages for analysis

## Voice Commands

- **Navigate**: "Navigate to [website]" or "Go to [website]"
- **Describe**: "Describe this page" or "What's on this page?"
- **Read**: "Read the content" or "Summarize this page"
- **Click**: "Click on [element]" or "Click [button name]"
- **Scroll**: "Scroll down/up" or "Scroll to top/bottom"
- **Navigation**: "Go back" or "Go forward"
- **Cookies**: "Accept cookies"
- **Help**: "Help" - lists all available commands

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Chrome browser installed
- Microphone for voice input
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/voice-web-assistant.git
   cd voice-web-assistant
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your OpenAI API key**
   
   Create a `.env` file in the root directory:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. **Run the assistant**
   ```bash
   python run.py
   ```

## How to Use

1. **Start the application** - A small window will appear
2. **Hold SPACE** to record your voice command
3. **Release SPACE** when you're done speaking
4. **Wait for response** - The assistant will execute your command and speak the result
5. **Press Left Shift** to stop any ongoing speech

### Tips for Best Results

- Speak clearly and naturally
- Wait for the "Ready" status before giving a new command
- For web searches, just say "Navigate to [your search query]"
- Use "describe" first on a new page to understand the layout

## Architecture

```
voice-web-assistant/
├── main_app.py          # Main application entry point
├── run.py               # Launcher script
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
│
├── services/            # Core service modules
│   ├── audio_service.py     # Voice recording & TTS
│   ├── browser_service.py   # Web browser control
│   ├── screenshot_service.py # Screenshot capture
│   └── vision_service.py    # GPT-4 Vision integration
│
├── core/                # Core logic
│   ├── command_processor.py # Voice command processing
│   └── config_manager.py    # Configuration management
│
├── ui/                  # User interface
│   ├── main_window.py   # Main GUI window
│   └── components.py    # UI components
│
└── utils/              # Utility modules
    ├── constants.py     # Application constants
    ├── file_manager.py  # File operations
    └── logger.py        # Logging utilities
```

## Configuration

### Audio Settings

The application uses Edge-TTS for fast text-to-speech. You can modify the voice in `audio_service.py`:

```python
# Change voice (line ~119)
communicate = self.edge_tts.Communicate(text, "en-US-AriaNeural")
# Other options: en-US-JennyNeural, en-US-GuyNeural, etc.
```

### Browser Settings

Browser options can be modified in `browser_service.py`. The application uses Chrome in non-headless mode by default.

## Troubleshooting

### Common Issues

1. **"No OpenAI API key found"**
   - Make sure you've created a `.env` file with your API key
   - Check that the key starts with `sk-`

2. **"Microphone not working"**
   - Check your system's microphone permissions
   - Ensure no other application is using the microphone

3. **"Chrome driver issues"**
   - The application auto-downloads the correct ChromeDriver
   - Make sure Chrome browser is installed and up to date

4. **"Edge-TTS not working"**
   - Requires internet connection
   - Will auto-install on first run

### Debug Mode

Enable detailed logging by setting the log level in your `.env`:
```
LOG_LEVEL=DEBUG
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for GPT-4 Vision API
- Microsoft for Edge-TTS
- Selenium WebDriver for browser automation
- All the open-source libraries that made this project possible

## Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Search existing [GitHub Issues](https://github.com/yourusername/voice-web-assistant/issues)
3. Create a new issue with detailed information about your problem

---

**Note**: This application requires an active internet connection for web browsing, voice transcription, and GPT-4 Vision API calls.