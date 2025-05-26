import os
from enum import Enum


class Environment(Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"


class Settings:
    def __init__(self):
        self.environment = Environment(os.getenv("ENVIRONMENT", "development"))
        self.debug = self.environment == Environment.DEVELOPMENT

        # API Keys
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")

        # Service URLs
        self.audio_service_url = os.getenv("AUDIO_SERVICE_URL", "http://localhost:8001")
        self.browser_service_url = os.getenv("BROWSER_SERVICE_URL", "http://localhost:8002")
        self.vision_service_url = os.getenv("VISION_SERVICE_URL", "http://localhost:8003")

        # Directories
        self.log_dir = os.getenv("LOG_DIR", "logs")
        self.temp_dir = os.getenv("TEMP_DIR", "temp")

        # Audio settings
        self.audio_chunk_size = int(os.getenv("AUDIO_CHUNK_SIZE", "1024"))
        self.audio_sample_rate = int(os.getenv("AUDIO_SAMPLE_RATE", "44100"))

        # Browser settings
        self.browser_headless = os.getenv("BROWSER_HEADLESS", "false").lower() == "true"

        # Create directories
        os.makedirs(self.log_dir, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)


settings = Settings()
