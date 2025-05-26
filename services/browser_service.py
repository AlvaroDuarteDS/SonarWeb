from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse
import time
import threading


class BrowserService:
    def __init__(self):
        self.driver = None
        self.current_url = None
        self.auto_cookies_enabled = False
        self.setup_webdriver()

    def setup_webdriver(self):
        """Setup Selenium WebDriver"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument("--disable-infobars")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--disable-features=VizDisplayCompositor")

            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            print("WebDriver initialized successfully")
        except Exception as e:
            print(f"Error setting up WebDriver: {e}")
            self.driver = None

    def enable_auto_cookies(self):
        """Enable automatic cookie acceptance for all pages"""
        self.auto_cookies_enabled = True
        print("✅ Auto-accept cookies enabled for all pages")

    def disable_auto_cookies(self):
        """Disable automatic cookie acceptance"""
        self.auto_cookies_enabled = False
        print("❌ Auto-accept cookies disabled")

    def _auto_accept_cookies_background(self):
        """Auto accept cookies in background if enabled"""
        if not self.auto_cookies_enabled:
            return

        def accept_task():
            time.sleep(3)  # Wait for page to load
            try:
                self.auto_accept_cookies()
            except:
                pass

        threading.Thread(target=accept_task, daemon=True).start()

    def navigate_to(self, website):
        """Navigate to website"""
        if not self.driver:
            return False, "Browser not available"

        try:
            website = website.strip()
            if not website:
                return False, "Empty website"

            # Add protocol if missing
            if not website.startswith(('http://', 'https://')):
                if "." in website and " " not in website:
                    website = "https://" + website
                else:
                    search_query = website.replace(" ", "+")
                    website = f"https://www.google.com/search?q={search_query}"

            self.driver.get(website)
            time.sleep(2)
            self.current_url = self.driver.current_url

            # Auto-accept cookies if enabled
            self._auto_accept_cookies_background()

            parsed_url = urlparse(self.current_url)
            domain = parsed_url.netloc or parsed_url.path
            return True, f"Navigated to {domain}"

        except Exception as e:
            return False, f"Navigation failed: {e}"

    def click_element(self, element_text):
        """Click on element by text with fuzzy matching"""
        if not self.driver:
            return False, "Browser not available"

        try:
            initial_url = self.driver.current_url
            search_text = element_text.lower().strip()
            search_text = search_text.replace("click on ", "").replace("click ", "")

            # Find clickable elements
            clickable_elements = []
            try:
                buttons = self.driver.find_elements(By.TAG_NAME, "button")
                links = self.driver.find_elements(By.TAG_NAME, "a")
                onclick_elements = self.driver.find_elements(By.XPATH, "//*[@onclick]")
                role_elements = self.driver.find_elements(By.XPATH, "//*[@role='button' or @role='link']")

                clickable_elements.extend(buttons + links + onclick_elements + role_elements)
            except Exception as e:
                return False, f"Error finding elements: {e}"

            # Find best match
            best_match = None
            best_score = 0

            for element in clickable_elements:
                try:
                    if not element.is_displayed() or not element.is_enabled():
                        continue

                    element_text_content = element.text.lower().strip()
                    if not element_text_content:
                        element_text_content = element.get_attribute('aria-label')
                        if element_text_content:
                            element_text_content = element_text_content.lower().strip()

                    if not element_text_content:
                        continue

                    # Calculate similarity
                    score = 0
                    if element_text_content == search_text:
                        score = 100
                    elif search_text in element_text_content:
                        score = 80
                    elif all(word in element_text_content for word in search_text.split()):
                        score = 60

                    if score > best_score:
                        best_score = score
                        best_match = element

                except:
                    continue

            # Click best match
            if best_match and best_score > 30:
                try:
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", best_match)
                    time.sleep(0.5)

                    matched_text = best_match.text or best_match.get_attribute('aria-label') or "element"

                    # Try multiple click methods
                    try:
                        best_match.click()
                    except:
                        try:
                            self.driver.execute_script("arguments[0].click();", best_match)
                        except:
                            self.driver.execute_script("""
                                var element = arguments[0];
                                var clickEvent = new MouseEvent('click', {
                                    view: window, bubbles: true, cancelable: true
                                });
                                element.dispatchEvent(clickEvent);
                            """, best_match)

                    time.sleep(1)

                    # Update URL if changed
                    if self.driver.current_url != initial_url:
                        self.current_url = self.driver.current_url
                        # Auto-accept cookies on new page
                        self._auto_accept_cookies_background()

                    return True, f"Clicked: {matched_text}"

                except Exception as e:
                    return False, f"Click failed: {e}"

            return False, "Element not found"

        except Exception as e:
            return False, f"Click error: {e}"

    def scroll_page(self, direction, amount="page"):
        """Scroll the page"""
        if not self.driver:
            return False, "Browser not available"

        try:
            if direction.lower() == "up":
                if amount == "top":
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    return True, "Scrolled to top"
                else:
                    self.driver.execute_script("window.scrollBy(0, -window.innerHeight);")
                    return True, "Scrolled up"
            else:
                if amount == "bottom":
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    return True, "Scrolled to bottom"
                else:
                    self.driver.execute_script("window.scrollBy(0, window.innerHeight);")
                    return True, "Scrolled down"

        except Exception as e:
            return False, f"Scroll error: {e}"

    def go_back(self):
        """Navigate back"""
        if not self.driver:
            return False, "Browser not available"

        try:
            self.driver.back()
            time.sleep(1)
            self.current_url = self.driver.current_url
            # Auto-accept cookies on back navigation
            self._auto_accept_cookies_background()
            return True, "Navigated back"
        except Exception as e:
            return False, f"Back navigation failed: {e}"

    def go_forward(self):
        """Navigate forward"""
        if not self.driver:
            return False, "Browser not available"

        try:
            self.driver.forward()
            time.sleep(1)
            self.current_url = self.driver.current_url
            # Auto-accept cookies on forward navigation
            self._auto_accept_cookies_background()
            return True, "Navigated forward"
        except Exception as e:
            return False, f"Forward navigation failed: {e}"

    def auto_accept_cookies(self):
        """Auto accept cookies with common patterns"""
        if not self.driver:
            return False, "Browser not available"

        try:
            accept_selectors = [
                "//button[contains(text(), 'Accept')]",
                "//button[contains(text(), 'I agree')]",
                "//button[contains(text(), 'Allow')]",
                "//button[contains(text(), 'OK')]",
                "//button[contains(text(), 'Got it')]",
                "//button[contains(@aria-label, 'Accept')]",
                "//button[contains(@class, 'accept')]",
                "//*[@role='button'][contains(text(), 'Accept')]",
                "//button[contains(@id, 'accept')]",
                "//button[contains(@class, 'cookie')]",
                "//a[contains(text(), 'Accept')]"
            ]

            for selector in accept_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            self.driver.execute_script("arguments[0].click();", element)
                            print("🍪 Cookies accepted automatically")
                            return True, "Cookies accepted"
                except:
                    continue

            return False, "No cookie popup found"

        except Exception as e:
            return False, f"Cookie acceptance failed: {e}"

    def get_current_domain(self):
        """Get current domain"""
        if self.current_url:
            parsed_url = urlparse(self.current_url)
            return parsed_url.netloc or parsed_url.path
        return "No site"

    def cleanup(self):
        """Clean up browser resources"""
        try:
            if self.driver:
                self.driver.quit()
        except:
            pass