import os
import uuid
import tempfile
from PIL import Image
import io
import time


class ScreenshotService:
    def __init__(self, browser_service, screenshot_temp_dir):
        self.browser_service = browser_service
        self.screenshot_temp_dir = screenshot_temp_dir
        self.last_screenshot_path = None

        if not os.path.exists(self.screenshot_temp_dir):
            os.makedirs(self.screenshot_temp_dir)

    def take_screenshot(self):
        """Take a simple screenshot"""
        if not self.browser_service.driver:
            return None

        try:
            screenshot_path = os.path.join(self.screenshot_temp_dir, f"screenshot_{uuid.uuid4()}.png")
            self.browser_service.driver.save_screenshot(screenshot_path)
            self.last_screenshot_path = screenshot_path
            return screenshot_path
        except Exception as e:
            print(f"Screenshot error: {e}")
            return None

    def take_full_page_screenshot(self):
        """Take a full page screenshot by scrolling and stitching"""
        if not self.browser_service.driver:
            return None

        try:
            driver = self.browser_service.driver

            # Store original state
            original_size = driver.get_window_size()
            original_scroll = driver.execute_script("return window.pageYOffset;")

            # Get page dimensions
            total_height = driver.execute_script(
                "return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);"
            )
            viewport_height = driver.execute_script("return window.innerHeight")

            screenshot_path = os.path.join(self.screenshot_temp_dir, f"screenshot_{uuid.uuid4()}.png")

            # Scroll to top
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(0.5)

            # Take first screenshot
            screenshot_binary = driver.get_screenshot_as_png()
            screenshot = Image.open(io.BytesIO(screenshot_binary))
            total_width = screenshot.width

            # If page fits in one screenshot
            if total_height <= viewport_height:
                screenshot.save(screenshot_path)
                self.last_screenshot_path = screenshot_path
                return screenshot_path

            # Create full screenshot canvas
            full_screenshot = Image.new('RGB', (total_width, total_height))
            full_screenshot.paste(screenshot, (0, 0))

            # Scroll and capture sections
            current_height = viewport_height
            while current_height < total_height:
                driver.execute_script(f"window.scrollTo(0, {current_height});")
                time.sleep(0.5)

                screenshot_binary = driver.get_screenshot_as_png()
                screenshot = Image.open(io.BytesIO(screenshot_binary))
                full_screenshot.paste(screenshot, (0, current_height))
                current_height += viewport_height

            # Save and restore state
            full_screenshot.save(screenshot_path)
            driver.set_window_size(original_size['width'], original_size['height'])
            driver.execute_script(f"window.scrollTo(0, {original_scroll});")

            self.last_screenshot_path = screenshot_path
            return screenshot_path

        except Exception as e:
            print(f"Full screenshot error: {e}")
            # Fallback to simple screenshot
            return self.take_screenshot()

    def cleanup_screenshots(self):
        """Clean up screenshot files"""
        try:
            if os.path.exists(self.screenshot_temp_dir):
                for file in os.listdir(self.screenshot_temp_dir):
                    try:
                        os.remove(os.path.join(self.screenshot_temp_dir, file))
                    except:
                        pass
        except:
            pass
