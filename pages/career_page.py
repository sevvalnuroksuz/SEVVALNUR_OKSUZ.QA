"""
Career Page Object Model
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CareerPage(BasePage):
    """Page Object for Career Page"""
    
    # Locators
    EXPLORE_OPEN_ROLES_BUTTON = (By.XPATH, "//a[contains(text(), 'Explore open roles')] | //button[contains(text(), 'Explore open roles')] | //*[contains(text(), 'Explore open roles')]")
    
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
            # Check URL or page title
            current_url = self.get_current_url()
            assert "career" in current_url.lower() or "hiring" in current_url.lower(), \
                f"Not on career page. Current URL: {current_url}"
            return True
        except AssertionError as e:
            self.screenshot_handler.take_screenshot(self.driver, "career_page_verification_failed")
            raise
    
    def verify_explore_open_roles_button(self) -> bool:
        """
        Verify that 'Explore open roles' button exists
        
        Returns:
            True if button exists
        """
        try:
            # Try multiple locator strategies
            locators = [
                (By.LINK_TEXT, "Explore open roles"),
                (By.PARTIAL_LINK_TEXT, "Explore open roles"),
                (By.XPATH, "//a[contains(text(), 'Explore open roles')]"),
                (By.XPATH, "//button[contains(text(), 'Explore open roles')]"),
                (By.XPATH, "//*[contains(text(), 'Explore open roles')]"),
            ]
            
            for by, value in locators:
                if self.is_element_present(by, value, timeout=5):
                    return True
            
            raise AssertionError("'Explore open roles' button not found")
        except AssertionError as e:
            self.screenshot_handler.take_screenshot(self.driver, "explore_button_verification_failed")
            raise
    
    def click_explore_open_roles(self):
        """Click on 'Explore open roles' button"""
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            # Wait for page to stabilize (reduced time)
            WebDriverWait(self.driver, 3).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            
            # Scroll page to find button
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            
            # Fast-path: try a direct clickable by text (case-insensitive) or href containing careers/jobs
            try:
                quick_xpath = "//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'explore open roles') or //button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'explore open roles')] | //a[contains(translate(@href, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'career') or contains(translate(@href, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'jobs') or contains(translate(@href, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'open') ]"
                elem = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, quick_xpath)))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
                try:
                    self.driver.execute_script("arguments[0].click();", elem)
                except:
                    elem.click()
                WebDriverWait(self.driver, 3).until(
                    lambda d: d.execute_script("return document.readyState") == "complete"
                )
                return
            except Exception:
                # fast-path failed -> fall back to robust strategies
                pass
            # Try multiple locator strategies with case-insensitive matching
            locators = [
                (By.LINK_TEXT, "Explore open roles"),
                (By.PARTIAL_LINK_TEXT, "Explore open roles"),
                (By.XPATH, "//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'explore open roles')]"),
                (By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'explore open roles')]"),
                (By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'explore open roles')]"),
                (By.XPATH, "//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'explore') and contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'roles')]"),
                (By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'explore') and contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'roles')]"),
            ]
            
            clicked = False
            for by, value in locators:
                try:
                    elements = self.driver.find_elements(by, value)
                    for element in elements:
                        if element.is_displayed():
                            # Scroll into view
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                            # Try JavaScript click (more reliable)
                            try:
                                self.driver.execute_script("arguments[0].click();", element)
                            except:
                                element.click()
                            clicked = True
                            # Wait for navigation with reduced timeout
                            WebDriverWait(self.driver, 3).until(
                                lambda d: d.execute_script("return document.readyState") == "complete"
                            )
                            return
                except:
                    continue
            
            # Strategy 2: Find all links/buttons and check text
            all_clickables = self.driver.find_elements(By.XPATH, "//a | //button")
            for element in all_clickables:
                try:
                    text = element.text.lower()
                    if 'explore' in text and 'open' in text and 'roles' in text:
                        if element.is_displayed():
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                            try:
                                self.driver.execute_script("arguments[0].click();", element)
                            except:
                                element.click()
                            clicked = True
                            WebDriverWait(self.driver, 5).until(
                                lambda d: d.execute_script("return document.readyState") == "complete"
                            )
                            # Wait for Software Development section to appear
                            WebDriverWait(self.driver, 3).until(
                                EC.presence_of_element_located((By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'software')]"))
                            )
                            return
                except:
                    continue
            
            if not clicked:
                # Debug info
                page_text = self.driver.find_element(By.TAG_NAME, "body").text[:1000]
                print(f"Page text snippet: {page_text}")
                raise Exception("Could not find 'Explore open roles' button")
        except Exception as e:
            self.screenshot_handler.take_screenshot(self.driver, "click_explore_open_roles_failed")
            raise