"""
Utility module for taking screenshots on test failures
"""
import os
from datetime import datetime
from selenium import webdriver


class ScreenshotHandler:
    """Handler for taking screenshots when tests fail"""
    
    def __init__(self, screenshot_dir: str = "screenshots"):
        """
        Initialize screenshot handler
        
        Args:
            screenshot_dir: Directory to save screenshots
        """
        self.screenshot_dir = screenshot_dir
        self._ensure_directory_exists()
    
    def _ensure_directory_exists(self):
        """Create screenshot directory if it doesn't exist"""
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)
    
    def take_screenshot(self, driver: webdriver, test_name: str = "test") -> str:
        """
        Take a screenshot and save it with timestamp
        
        Args:
            driver: Selenium WebDriver instance
            test_name: Name of the test for filename
            
        Returns:
            Path to the saved screenshot
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{test_name}_{timestamp}.png"
        filepath = os.path.join(self.screenshot_dir, filename)
        
        try:
            # Check if driver is still valid
            if driver is None:
                print("Driver is None, cannot take screenshot")
                return ""
            
            # Try to take screenshot with timeout
            driver.save_screenshot(filepath)
            print(f"Screenshot saved: {filepath}")
            return filepath
        except Exception as e:
            # Don't raise exception, just log it
            print(f"Failed to take screenshot: {e}")
            return ""

