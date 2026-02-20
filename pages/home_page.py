"""
Home Page Object Model
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage


class HomePage(BasePage):
    """Page Object for Insider One Homepage"""

    WE_ARE_HIRING_LINK = (By.CSS_SELECTOR, "a[href='/careers/']")
    WE_ARE_HIRING_LINK_FALLBACK = (By.CSS_SELECTOR, "a[data-text=\"We're hiring\"]")

    def __init__(self, driver, screenshot_handler=None):
        """Initialize HomePage"""
        super().__init__(driver, screenshot_handler)

    def verify_homepage(self) -> bool:
        """
        Verify that we are on the Insider One homepage

        Returns:
            True if on homepage
        """
        try:
            current_url = self.get_current_url().lower()
            assert "insiderone.com" in current_url, f"Not on homepage. Current URL: {current_url}"
            return True
        except AssertionError:
            self.screenshot_handler.take_screenshot(self.driver, "homepage_verification_failed")
            raise

    def _safe_click(self, locator, timeout: int = 10):
        """
        Scroll element into view, then try a normal click.
        Falls back to JavaScript click if the element is intercepted.

        Args:
            locator: (By, value) tuple
            timeout: Maximum wait time in seconds
        """
        wait = WebDriverWait(self.driver, timeout)
        element = wait.until(EC.presence_of_element_located(locator))

        
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

        
        import time
        time.sleep(0.5)

        try:
            wait.until(EC.element_to_be_clickable(locator)).click()
        except Exception:
            
            self.driver.execute_script("arguments[0].click();", element)

    def click_we_are_hiring(self):
        """Click on 'We're hiring' link"""
        try:
            
            locator = (
                self.WE_ARE_HIRING_LINK
                if self.is_element_present(*self.WE_ARE_HIRING_LINK, timeout=3)
                else self.WE_ARE_HIRING_LINK_FALLBACK
            )

            self._safe_click(locator, timeout=10)

            # Confirm 
            self.wait_for_url_contains("/careers", timeout=10)

        except TimeoutException:
            self.screenshot_handler.take_screenshot(self.driver, "click_we_are_hiring_timeout")
            raise
        except Exception:
            self.screenshot_handler.take_screenshot(self.driver, "click_we_are_hiring_failed")
            raise