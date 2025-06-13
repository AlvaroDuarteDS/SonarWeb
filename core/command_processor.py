class CommandProcessor:
    def __init__(self, browser_service, audio_service, vision_service, screenshot_service):
        self.browser_service = browser_service
        self.audio_service = audio_service
        self.vision_service = vision_service
        self.screenshot_service = screenshot_service

    def process_command(self, text, status_callback=None):
        """Process voice command - returns (success, should_analyze_background)"""
        text = text.lower().strip()

        try:
            # Navigation commands - should trigger background analysis
            if any(keyword in text for keyword in ["navigate to", "go to", "open"]):
                website = self._extract_website(text)
                success, message = self.browser_service.navigate_to(website)
                self.audio_service.speak(message if success else "Navigation failed", status_callback)
                return (success, True)  # Should analyze on navigation

            # Description commands - don't analyze if using cache
            elif any(keyword in text for keyword in ["describe", "explain", "tell me about"]):
                success, used_cache = self._handle_describe_page(status_callback)
                return (success, not used_cache)  # Only analyze if didn't use cache

            # Content reading commands - don't analyze if using cache
            elif any(keyword in text for keyword in ["read", "summarize", "main content"]):
                success, used_cache = self._handle_read_content(status_callback)
                return (success, not used_cache)  # Only analyze if didn't use cache

            # Click commands - should trigger analysis as page might change
            elif "click" in text:
                element_text = text.replace("click on", "").replace("click", "").strip()
                if element_text:
                    success, message = self.browser_service.click_element(element_text)
                    self.audio_service.speak(message, status_callback)
                    return (success, True)  # Should analyze after click
                else:
                    self.audio_service.speak("What should I click?", status_callback)
                    return (False, False)

            # Scroll commands - no analysis needed
            elif "scroll" in text:
                success = self._handle_scroll(text, status_callback)
                return (success, False)  # No analysis needed for scroll

            # Navigation commands - should trigger analysis
            elif "back" in text:
                success, message = self.browser_service.go_back()
                self.audio_service.speak(message, status_callback)
                return (success, True)  # Should analyze after navigation

            elif "forward" in text:
                success, message = self.browser_service.go_forward()
                self.audio_service.speak(message, status_callback)
                return (success, True)  # Should analyze after navigation

            # Cookie commands - no analysis needed
            elif "accept cookies" in text or "accept cookie" in text:
                success, message = self.browser_service.auto_accept_cookies()
                self.audio_service.speak(message, status_callback)
                return (success, False)  # No analysis for cookie acceptance

            # Help command - no analysis needed
            elif "help" in text:
                self.audio_service.speak(
                    "Available commands: navigate to, describe, read, click on, scroll, back, forward, accept cookies, help",
                    status_callback
                )
                return (True, False)

            # Unknown command
            else:
                self.audio_service.speak("Command not recognized", status_callback)
                return (False, False)

        except Exception as e:
            print(f"Command processing error: {e}")
            self.audio_service.speak("Command failed", status_callback)
            return (False, False)

    def _extract_website(self, text):
        """Extract website from navigation command"""
        for keyword in ["navigate to", "go to", "open"]:
            if keyword in text:
                return text.split(keyword, 1)[1].strip()
        return ""

    def _handle_describe_page(self, status_callback):
        """Handle page description - returns (success, used_cache)"""
        if not self.browser_service.current_url:
            self.audio_service.speak("Not on any webpage", status_callback)
            return (False, False)

        current_url = self.browser_service.current_url

        # Check if we have cached description
        if current_url in self.vision_service.description_cache:
            description = self.vision_service.description_cache[current_url]
            self.audio_service.speak(description, status_callback)
            print(f"📋 Used cached description for {current_url} - no new analysis needed")
            return (True, True)  # Success and used cache

        # No cache, analyze now
        if status_callback:
            status_callback("Analyzing page...")

        screenshot_path = self.screenshot_service.take_full_page_screenshot()
        if screenshot_path:
            description = self.vision_service.get_page_description(screenshot_path, current_url)
            if description:
                self.audio_service.speak(description, status_callback)
                return (True, False)  # Success but didn't use cache
            else:
                self.audio_service.speak("Cannot analyze page", status_callback)
        else:
            self.audio_service.speak("Cannot capture page", status_callback)

        return (False, False)

    def _handle_read_content(self, status_callback):
        """Handle content reading - returns (success, used_cache)"""
        if not self.browser_service.current_url:
            self.audio_service.speak("Not on any webpage", status_callback)
            return (False, False)

        current_url = self.browser_service.current_url

        # Check if we have cached content
        if current_url in self.vision_service.content_cache:
            content = self.vision_service.content_cache[current_url]
            self.audio_service.speak(content, status_callback)
            print(f"📋 Used cached content for {current_url} - no new analysis needed")
            return (True, True)  # Success and used cache

        # No cache, analyze now
        if status_callback:
            status_callback("Reading content...")

        screenshot_path = self.screenshot_service.take_screenshot()
        if screenshot_path:
            content = self.vision_service.get_main_content(screenshot_path, current_url)
            if content:
                self.audio_service.speak(content, status_callback)
                return (True, False)  # Success but didn't use cache
            else:
                self.audio_service.speak("Cannot read content", status_callback)
        else:
            self.audio_service.speak("Cannot capture page", status_callback)

        return (False, False)

    def _handle_scroll(self, text, status_callback):
        """Handle scroll commands"""
        if "up" in text:
            amount = "top" if "to top" in text else "page"
            success, message = self.browser_service.scroll_page("up", amount)
        elif "down" in text:
            amount = "bottom" if "to bottom" in text else "page"
            success, message = self.browser_service.scroll_page("down", amount)
        else:
            self.audio_service.speak("Specify scroll direction", status_callback)
            return False

        self.audio_service.speak(message, status_callback)
        return success