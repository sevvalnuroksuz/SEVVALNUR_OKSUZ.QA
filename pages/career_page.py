"""
Career Page Object Model
"""
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage


class CareerPage(BasePage):
    """Page Object for Career Page"""

    #  stabil locator 
    EXPLORE_OPEN_ROLES_BUTTON = (By.CSS_SELECTOR, "a[href='#open-roles']")

    def __init__(self, driver, screenshot_handler=None):
        """Initialize CareerPage"""
        super().__init__(driver, screenshot_handler)

    def verify_career_page(self) -> bool:
        """
        Verify that we are on the Career page

        Returns:
            True if on career page
        """
        try:
            current_url = self.get_current_url()
            assert (
                "career" in current_url.lower()
                or "hiring" in current_url.lower()
                or "careers" in current_url.lower()
            ), f"Not on career page. Current URL: {current_url}"
            return True
        except AssertionError:
            self.screenshot_handler.take_screenshot(self.driver, "career_page_verification_failed")
            raise

    def verify_explore_open_roles_button(self) -> bool:
        """
        Verify that 'Explore open roles' button exists

        Returns:
            True if button exists
        """
        try:
            return self.is_element_present(*self.EXPLORE_OPEN_ROLES_BUTTON, timeout=5)
        except Exception:
            self.screenshot_handler.take_screenshot(self.driver, "explore_button_verification_failed")
            raise

    def click_explore_open_roles(self):
        """Click on 'Explore open roles' button"""
        try:
            
            self.click_element(*self.EXPLORE_OPEN_ROLES_BUTTON, timeout=5)

        
            #  Doğrulama: URL içinde open-roles bekle.
            self.wait_for_url_contains("#open-roles", timeout=5)

        except TimeoutException:
            self.screenshot_handler.take_screenshot(self.driver, "click_explore_open_roles_timeout")
            raise
        except Exception:
            self.screenshot_handler.take_screenshot(self.driver, "click_explore_open_roles_failed")
            raise
