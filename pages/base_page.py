"""
Base Page Object Model class
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.screenshot_handler import ScreenshotHandler


class BasePage:
    """Base class for all page objects"""
    
    def __init__(self, driver: webdriver, screenshot_handler: ScreenshotHandler = None):
        """
        Initialize base page
        
        Args:
            driver: Selenium WebDriver instance
            screenshot_handler: Screenshot handler instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.screenshot_handler = screenshot_handler or ScreenshotHandler()
    
    def find_element(self, by: By, value: str, timeout: int = 10):
        """
        Find element with explicit wait
        
        Args:
            by: Locator strategy
            value: Locator value
            timeout: Maximum wait time in seconds
            
        Returns:
            WebElement
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.presence_of_element_located((by, value)))
        except TimeoutException:
            self.screenshot_handler.take_screenshot(self.driver, "element_not_found")
            raise
    
    def find_elements(self, by: By, value: str, timeout: int = 10):
        """
        Find multiple elements with explicit wait
        
        Args:
            by: Locator strategy
            value: Locator value
            timeout: Maximum wait time in seconds
            
        Returns:
            List of WebElements
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.presence_of_element_located((by, value)))
            return self.driver.find_elements(by, value)
        except TimeoutException:
            self.screenshot_handler.take_screenshot(self.driver, "elements_not_found")
            raise
    
    def click_element(self, by: By, value: str, timeout: int = 10):
        """
        Click on element with explicit wait
        
        Args:
            by: Locator strategy
            value: Locator value
            timeout: Maximum wait time in seconds
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.element_to_be_clickable((by, value)))
            element.click()
        except TimeoutException:
            self.screenshot_handler.take_screenshot(self.driver, "click_failed")
            raise
    
    def get_text(self, by: By, value: str, timeout: int = 10) -> str:
        """
        Get text from element
        
        Args:
            by: Locator strategy
            value: Locator value
            timeout: Maximum wait time in seconds
            
        Returns:
            Element text
        """
        try:
            element = self.find_element(by, value, timeout)
            return element.text
        except TimeoutException:
            self.screenshot_handler.take_screenshot(self.driver, "get_text_failed")
            raise
    
    def is_element_present(self, by: By, value: str, timeout: int = 10) -> bool:
        """
        Check if element is present
        
        Args:
            by: Locator strategy
            value: Locator value
            timeout: Maximum wait time in seconds
            
        Returns:
            True if element is present, False otherwise
        """
        try:
            self.find_element(by, value, timeout)
            return True
        except TimeoutException:
            return False
    
    def wait_for_url_contains(self, url_part: str, timeout: int = 10):
        """
        Wait for URL to contain specific string
        
        Args:
            url_part: String that should be in URL
            timeout: Maximum wait time in seconds
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.url_contains(url_part))
        except TimeoutException:
            self.screenshot_handler.take_screenshot(self.driver, "url_check_failed")
            raise
    
    def get_current_url(self) -> str:
        """Get current page URL"""
        return self.driver.current_url