import base64
import openai
import json
import os
import threading
import time
from typing import Optional, Dict


class VisionService:
    def __init__(self):
        self.openai_client = None
        self.description_cache: Dict[str, str] = {}
        self.content_cache: Dict[str, str] = {}
        self.processing_queue = []
        self.setup_openai()

        # Start background processor
        self.background_thread = threading.Thread(target=self._background_processor, daemon=True)
        self.background_thread.start()

    def setup_openai(self):
        """Setup OpenAI client"""
        try:
            openai_api_key = None

            config_paths = [
                'config.json',
                '../config.json',
                './config/config.json',
                os.path.join(os.path.dirname(__file__), '..', 'config.json'),
                os.path.join(os.getcwd(), 'config.json')
            ]

            for config_path in config_paths:
                try:
                    if os.path.exists(config_path):
                        with open(config_path, 'r') as config_file:
                            config = json.load(config_file)
                            openai_api_key = config.get('OPENAI_API_KEY')
                            if openai_api_key:
                                break
                except Exception as e:
                    continue

            if not openai_api_key:
                openai_api_key = os.getenv('OPENAI_API_KEY')

            if openai_api_key and openai_api_key.startswith('sk-'):
                self.openai_client = openai.OpenAI(api_key=openai_api_key)
                print("✅ OpenAI API initialized successfully")
            else:
                print("❌ OpenAI API key not found")

        except Exception as e:
            print(f"Error initializing OpenAI: {e}")

    def queue_background_analysis(self, url: str, screenshot_path: str):
        """Queue screenshot for background analysis"""
        if not self.openai_client:
            return

        print(f"🔄 Queuing background analysis for: {url}")
        self.processing_queue.append({
            'url': url,
            'screenshot_path': screenshot_path,
            'timestamp': time.time()
        })

    def _background_processor(self):
        """Process screenshots in background"""
        while True:
            if self.processing_queue:
                task = self.processing_queue.pop(0)
                try:
                    url = task['url']
                    screenshot_path = task['screenshot_path']

                    print(f"🤖 Processing in background: {url}")

                    # Generate both description and content
                    description = self._analyze_screenshot(screenshot_path, "describe")
                    content = self._analyze_screenshot(screenshot_path, "content")

                    if description:
                        self.description_cache[url] = description
                        print(f"✅ Cached description for: {url}")

                    if content:
                        self.content_cache[url] = content
                        print(f"✅ Cached content for: {url}")

                    # Clean up screenshot
                    try:
                        os.remove(screenshot_path)
                    except:
                        pass

                except Exception as e:
                    print(f"Error in background processing: {e}")

            time.sleep(1)  # Check every second

    def get_page_description(self, screenshot_path: str, url: str = None) -> str:
        """Get page description - check cache first"""
        if url and url in self.description_cache:
            print("📋 Using cached description")
            return self.description_cache[url]

        # Not in cache, analyze now
        description = self._analyze_screenshot(screenshot_path, "describe")

        if description and url:
            self.description_cache[url] = description

        return description or "Could not analyze page"

    def get_main_content(self, screenshot_path: str, url: str = None) -> str:
        """Get main content - check cache first"""
        if url and url in self.content_cache:
            print("📋 Using cached content")
            return self.content_cache[url]

        # Not in cache, analyze now
        content = self._analyze_screenshot(screenshot_path, "content")

        if content and url:
            self.content_cache[url] = content

        return content or "Could not read content"

    def _analyze_screenshot(self, screenshot_path: str, analysis_type: str) -> Optional[str]:
        """Analyze screenshot with OpenAI"""
        if not self.openai_client:
            return "OpenAI not configured"

        try:
            base64_image = self.encode_image_to_base64(screenshot_path)
            if not base64_image:
                return None

            if analysis_type == "describe":
                prompt = "Describe this webpage briefly. Focus on key navigation elements and main content. Keep it concise."
            else:  # content
                prompt = "Summarize the main content of this page. Ignore menus, ads, and navigation. Be brief and direct."

            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{
                    "role": "user",
                    "content": [{
                        "type": "text",
                        "text": prompt
                    }, {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{base64_image}"}
                    }]
                }],
                max_tokens=300
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"OpenAI analysis error: {e}")
            return f"Error analyzing: {str(e)}"

    def encode_image_to_base64(self, image_path):
        """Encode image to base64"""
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            print(f"Image encoding error: {e}")
            return None

    def clear_cache(self):
        """Clear all caches"""
        self.description_cache.clear()
        self.content_cache.clear()
        print("🗑️ Cache cleared")