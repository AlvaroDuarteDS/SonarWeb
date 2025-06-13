import time
import tkinter as tk
import threading
import tempfile
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.audio_service import AudioService
from services.browser_service import BrowserService
from services.vision_service import VisionService
from services.screenshot_service import ScreenshotService
from core.command_processor import CommandProcessor
from ui.main_window import MainWindow


class VoiceWebAssistant:
    def __init__(self):
        self._exiting = False
        self.recording = False

        # Setup temp directories
        self.speech_temp_dir = os.path.join(tempfile.gettempdir(), "web_assistant_speech")
        self.screenshot_temp_dir = os.path.join(tempfile.gettempdir(), "web_assistant_screenshots")

        # Initialize services
        self.audio_service = AudioService(self.speech_temp_dir)
        self.browser_service = BrowserService()
        self.vision_service = VisionService()
        self.screenshot_service = ScreenshotService(self.browser_service, self.screenshot_temp_dir)
        self.command_processor = CommandProcessor(
            self.browser_service, self.audio_service,
            self.vision_service, self.screenshot_service
        )

        # Setup UI
        self.main_window = MainWindow(self)

    def start_recording(self, event=None):
        """Start recording when space is pressed"""
        if self.recording:
            return

        if self.audio_service.start_recording():
            self.recording = True
            self.main_window.update_status("🔴 Recording...")
            threading.Thread(target=self._record_audio_thread, daemon=True).start()

    def stop_recording(self, event=None):
        """Stop recording when space is released"""
        if self.recording:
            self.audio_service.stop_recording()
            self.recording = False

    def force_stop_recording(self, event=None):
        """Force stop recording with Left Shift"""
        if self.recording:
            self.audio_service.stop_recording()
            self.recording = False
            self.main_window.update_status("⏹️ Recording stopped")

        # Also stop any ongoing speech
        self.audio_service.stop_speaking()
        self.main_window.update_status("🔇 Speech stopped")

    def _record_audio_thread(self):
        """Handle audio recording in separate thread"""
        try:
            # Record audio
            audio_file = self.audio_service.record_audio()

            if audio_file:
                self.main_window.update_status("🔄 Processing...")

                # Transcribe
                text = self.audio_service.transcribe_audio(audio_file)

                if text:
                    print(f"Command: {text}")

                    # Process command - modified to return tuple
                    result = self.command_processor.process_command(text, self.main_window.update_status)

                    # Handle result based on type
                    if isinstance(result, tuple):
                        success, should_analyze = result
                    else:
                        # Backwards compatibility
                        success = result
                        should_analyze = True

                    # Update site display
                    if success and self.browser_service.current_url:
                        domain = self.browser_service.get_current_domain()
                        self.main_window.update_current_site(f"📍 {domain}")

                        # Only trigger background analysis for navigation commands or when needed
                        if should_analyze:
                            self._trigger_background_analysis()

                else:
                    self.audio_service.speak("Didn't catch that", self.main_window.update_status)
            else:
                self.main_window.update_status("Ready")

        except Exception as e:
            print(f"Recording thread error: {e}")
            self.main_window.update_status("Ready")

    def _trigger_background_analysis(self):
        """Trigger background screenshot analysis"""

        def background_task():
            try:
                time.sleep(2)  # Wait for page to settle
                screenshot_path = self.screenshot_service.take_full_page_screenshot()
                if screenshot_path and self.browser_service.current_url:
                    # Don't delete the screenshot yet - let vision service handle it
                    screenshot_copy = screenshot_path + "_analysis"
                    import shutil
                    shutil.copy2(screenshot_path, screenshot_copy)

                    self.vision_service.queue_background_analysis(
                        self.browser_service.current_url,
                        screenshot_copy
                    )
            except Exception as e:
                print(f"Background analysis error: {e}")

        threading.Thread(target=background_task, daemon=True).start()

    def auto_accept_cookies(self):
        """Toggle auto accept cookies"""
        if self.browser_service.auto_cookies_enabled:
            self.browser_service.disable_auto_cookies()
            self.audio_service.speak("Auto cookies disabled", self.main_window.update_status)
            self.main_window.update_cookies_button("🍪 Enable Auto Cookies")
        else:
            self.browser_service.enable_auto_cookies()
            self.audio_service.speak("Auto cookies enabled for all pages", self.main_window.update_status)
            self.main_window.update_cookies_button("🍪 Disable Auto Cookies")

    def take_manual_screenshot(self):
        """Manual screenshot for testing"""
        self.main_window.update_status("Taking screenshot...")
        path = self.screenshot_service.take_full_page_screenshot()
        if path:
            self.audio_service.speak("Screenshot captured", self.main_window.update_status)
        else:
            self.audio_service.speak("Screenshot failed", self.main_window.update_status)

    def refresh_page(self):
        """Refresh current page"""
        if self.browser_service.driver and self.browser_service.current_url:
            self.browser_service.driver.refresh()
            self.audio_service.speak("Page refreshed", self.main_window.update_status)
            # Clear cache for this URL since we refreshed
            if self.browser_service.current_url in self.vision_service.description_cache:
                del self.vision_service.description_cache[self.browser_service.current_url]
            if self.browser_service.current_url in self.vision_service.content_cache:
                del self.vision_service.content_cache[self.browser_service.current_url]
            # Trigger background analysis after refresh
            self._trigger_background_analysis()
        else:
            self.audio_service.speak("No page to refresh", self.main_window.update_status)

    def clear_cache(self):
        """Clear vision cache"""
        self.vision_service.clear_cache()
        self.audio_service.speak("Cache cleared", self.main_window.update_status)

    def exit_program(self, event=None):
        """Clean exit"""
        if self._exiting:
            return

        self._exiting = True
        self.main_window.update_status("Exiting...")

        # Cleanup services
        self.audio_service.cleanup()
        self.browser_service.cleanup()
        self.screenshot_service.cleanup_screenshots()

        try:
            self.main_window.root.quit()
        except:
            pass

    def run(self):
        """Run the application"""
        self.audio_service.speak("Voice assistant ready", self.main_window.update_status)

        try:
            self.main_window.root.mainloop()
        except Exception as e:
            print(f"Main loop error: {e}")