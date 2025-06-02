import os
import sys
from pathlib import Path

class SecureConfig:
    def __init__(self):
        self.openai_api_key = None
        self._load_api_key()
    
    def _load_api_key(self):
        """Load API key from multiple sources in order of preference"""
        
        # 1. Environment variable (production)
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if self.openai_api_key:
            print("✅ API key loaded from environment variable")
            return
        
        # 2. .env file (development)
        env_file = Path('.env')
        if env_file.exists():
            try:
                with open(env_file, 'r') as f:
                    for line in f:
                        if line.startswith('OPENAI_API_KEY='):
                            self.openai_api_key = line.split('=', 1)[1].strip()
                            print("✅ API key loaded from .env file")
                            return
            except Exception as e:
                print(f"⚠️ Error reading .env file: {e}")
        
        # 3. config.json (legacy support)
        config_file = Path('config.json')
        if config_file.exists():
            try:
                import json
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    self.openai_api_key = config.get('OPENAI_API_KEY')
                    if self.openai_api_key:
                        print("✅ API key loaded from config.json")
                        return
            except Exception as e:
                print(f"⚠️ Error reading config.json: {e}")
        
        # 4. No key found
        print("❌ No OpenAI API key found!")
        print("Please set OPENAI_API_KEY environment variable or create .env file")
        
    def validate_api_key(self):
        """Validate API key format"""
        if not self.openai_api_key:
            return False
        
        # OpenAI keys start with 'sk-' and have specific length
        if not self.openai_api_key.startswith('sk-'):
            print("❌ Invalid API key format: must start with 'sk-'")
            return False
        
        if len(self.openai_api_key) < 40:
            print("❌ Invalid API key format: too short")
            return False
        
        return True

# Global instance
secure_config = SecureConfig()
