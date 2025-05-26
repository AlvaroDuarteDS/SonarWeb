# Audio constants
CHUNK_SIZE = 1024
SAMPLE_RATE = 44100
CHANNELS = 1
AUDIO_FORMAT = 16  # pyaudio.paInt16

# UI constants
WINDOW_TITLE = "Voice Web Assistant"
DEFAULT_WINDOW_SIZE = "500x300"

# Temp directories
SPEECH_TEMP_DIR = "web_assistant_speech"
SCREENSHOT_TEMP_DIR = "web_assistant_screenshots"

# API endpoints (for microservices)
AUDIO_SERVICE_URL = "http://localhost:8001"
BROWSER_SERVICE_URL = "http://localhost:8002"
VISION_SERVICE_URL = "http://localhost:8003"
API_GATEWAY_URL = "http://localhost:8000"

# Timeouts
HTTP_TIMEOUT = 30
SELENIUM_TIMEOUT = 10
RECORDING_TIMEOUT = 30

# File extensions
SUPPORTED_AUDIO_FORMATS = ['.wav', '.mp3', '.flac']
SUPPORTED_IMAGE_FORMATS = ['.png', '.jpg', '.jpeg']