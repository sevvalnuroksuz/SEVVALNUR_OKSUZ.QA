"""
Home Page Object Model
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class HomePage(BasePage):
    """Page Object for Insider One Homepage"""
    
    # Locators
    WE_ARE_HIRING_LINK = (By.XPATH, "//a[contains(text(), \"We're hiring\")] | //*[contains(text(), \"We're hiring\")]")
    
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
            from selenium.webdriver.support.ui import WebDriverWait
            
            # Wait for page to load (optimized)
            WebDriverWait(self.driver, 5).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            
            # Check if URL contains insiderone.com
            current_url = self.get_current_url()
            assert "insiderone.com" in current_url.lower(), f"Not on homepage. Current URL: {current_url}"
            return True
        except AssertionError as e:
            self.screenshot_handler.take_screenshot(self.driver, "homepage_verification_failed")
            raise
    
    def click_we_are_hiring(self):
        """Click on 'We're hiring' link"""
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            # Wait for page to stabilize (optimized)
            WebDriverWait(self.driver, 2).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            
            # Scroll to find the link (it might be below the fold)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.driver.execute_script("window.scrollTo(0, 0);")
            
            # Fast-path: try to find a link whose href contains career/hiring/jobs (case-insensitive)
            try:
                quick_xpath = "//a[contains(translate(@href, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'career') or contains(translate(@href, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'hiring') or contains(translate(@href, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'careers') or contains(translate(@href, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'jobs')]"
                elem = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, quick_xpath)))
                self.driver.execute_script("arguments[0].scrollIntoView(true);", elem)
                try:
                    self.driver.execute_script("arguments[0].click();", elem)
                except:
                    elem.click()
                WebDriverWait(self.driver, 3).until(
                    lambda d: d.execute_script("return document.readyState") == "complete"
                )
                return
            except Exception:
                # fast-path failed -> continue to existing, more robust strategies
                pass
            
            # Try multiple locator strategies with case-insensitive matching
            locators = [
                # Exact matches
                (By.LINK_TEXT, "We're hiring"),
                (By.LINK_TEXT, "We are hiring"),
                (By.PARTIAL_LINK_TEXT, "hiring"),
                # XPath with various text variations
                (By.XPATH, "//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), \"we're hiring\")]"),
                (By.XPATH, "//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), \"we are hiring\")]"),
                (By.XPATH, "//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'hiring')]"),
                (By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), \"we're hiring\")]"),
                (By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), \"we are hiring\")]"),
                (By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'hiring')]"),
                # Button variations
                (By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'hiring')]"),
                # Generic link with href containing career/hiring
                (By.XPATH, "//a[contains(translate(@href, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'career') or contains(translate(@href, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'hiring')]"),
            ]
            
            clicked = False
            for by, value in locators:
                try:
                    elements = self.driver.find_elements(by, value)
                    for element in elements:
                        try:
                            # Check if element is visible and contains "hiring" text
                            if element.is_displayed():
                                element_text = element.text.lower()
                                if 'hiring' in element_text or 'career' in element_text:
                                    # Scroll into view
                                    self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                                    # Try JavaScript click first (more reliable)
                                    try:
                                        self.driver.execute_script("arguments[0].click();", element)
                                    except:
                                        element.click()
                                    clicked = True
                                    # Wait for navigation (optimized)
                                    WebDriverWait(self.driver, 3).until(
                                        lambda d: d.execute_script("return document.readyState") == "complete"
                                    )
                                    return
                        except:
                            continue
                except:
                    continue
            
            # Strategy 2: Find all links and check text content
            all_links = self.driver.find_elements(By.TAG_NAME, "a")
            for link in all_links:
                try:
                    link_text = link.text.lower()
                    link_href = link.get_attribute("href") or ""
                    if ('hiring' in link_text or 'career' in link_text or 
                        'hiring' in link_href.lower() or 'career' in link_href.lower()):
                        if link.is_displayed():
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", link)
                            try:
                                self.driver.execute_script("arguments[0].click();", link)
                            except:
                                link.click()
                            clicked = True
                            WebDriverWait(self.driver, 3).until(
                                lambda d: d.execute_script("return document.readyState") == "complete"
                            )
                            return
                except:
                    continue
            
            # Strategy 3: Find all clickable elements with "hiring" text
            all_elements = self.driver.find_elements(By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'hiring')]")
            for element in all_elements:
                try:
                    if element.is_displayed() and (element.tag_name == 'a' or element.tag_name == 'button' or element.get_attribute("onclick")):
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                        try:
                            self.driver.execute_script("arguments[0].click();", element)
                        except:
                            element.click()
                        clicked = True
                        WebDriverWait(self.driver, 3).until(
                            lambda d: d.execute_script("return document.readyState") == "complete"
                        )
                        return
                except:
                    continue
            
            if not clicked:
                # Debug: Print page text to help identify the issue
                page_text = self.driver.find_element(By.TAG_NAME, "body").text
                print(f"Page text snippet (first 3000 chars): {page_text[:3000]}")
                self.screenshot_handler.take_screenshot(self.driver, "click_we_are_hiring_failed")
                raise Exception("Could not find 'We're hiring' link")
        except Exception as e:
            self.screenshot_handler.take_screenshot(self.driver, "click_we_are_hiring_failed")
            raise