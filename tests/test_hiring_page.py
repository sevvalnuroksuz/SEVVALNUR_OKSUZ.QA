"""
Test case for hiring page automation
"""
import unittest
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import BASE_URL, SCREENSHOT_DIR
from pages.home_page import HomePage
from pages.career_page import CareerPage
from pages.job_listing_page import JobListingPage
from utils.screenshot_handler import ScreenshotHandler


class TestHiringPage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)

        # speed tweaks
        chrome_options.page_load_strategy = "eager"
        prefs = {
            "profile.managed_default_content_settings.images": 2,
            "profile.default_content_setting_values.notifications": 2,
        }
        chrome_options.add_experimental_option("prefs", prefs)

        # log azalt (opsiyonel)
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--disable-background-networking")
        chrome_options.add_argument("--disable-default-apps")
        chrome_options.add_argument("--disable-sync")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--disable-gpu")

        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(0)
        cls.screenshot_handler = ScreenshotHandler(SCREENSHOT_DIR)

    @classmethod
    def tearDownClass(cls):
        if cls.driver:
            cls.driver.quit()

    def setUp(self):
        self.driver.get(BASE_URL)

    def tearDown(self):
        if hasattr(self, "_outcome"):
            result = self._outcome.result
            if result.errors or result.failures:
                self.screenshot_handler.take_screenshot(self.driver, f"failed_{self._testMethodName}")

    def test_hiring_page_automation(self):
        try:
            home_page = HomePage(self.driver, self.screenshot_handler)
            home_page.verify_homepage()
            print("✓ Step 1: Verified Insider One homepage")

            home_page.click_we_are_hiring()
            career_page = CareerPage(self.driver, self.screenshot_handler)
            career_page.verify_career_page()
            print("✓ Step 2: Clicked 'We're hiring' and verified Career page")

            career_page.verify_explore_open_roles_button()
            print("✓ Step 3: Verified 'Explore open roles' button exists")

            career_page.click_explore_open_roles()
            print("✓ Step 4: Clicked 'Explore open roles' button")

            job_listing_page = JobListingPage(self.driver, self.screenshot_handler)
            job_listing_page.click_software_development_open_positions()
            print("✓ Step 5: Clicked 'Open Positions' under Software Development")

            # Step 6-7 tek seferde (hız)
            job_listing_page.apply_filters(location="Istanbul, Turkiye", team="Quality Assurance")
            print("✓ Step 6-7: Applied Location='Istanbul, Turkiye' and Team='Quality Assurance'")

            job_listing_page.verify_job_listings_displayed()
            print("✓ Step 8: Verified job listings are displayed")

            job_listing_page.verify_job_listings_content(expected_team="Quality Assurance", expected_location_substr="Istanbul")
            print("✓ Step 9: Verified listings contain 'Quality Assurance' and 'Istanbul'")

            job_listing_page.click_apply_button()
            job_listing_page.verify_lever_application_form()
            print("✓ Step 10: Clicked Apply -> Apply for this job and verified Lever Application Form")

            print("\n✅ All test steps completed successfully!")

        except Exception as e:
            self.screenshot_handler.take_screenshot(self.driver, "test_failure")
            print(f"\n❌ Test failed: {str(e)}")
            raise


if __name__ == "__main__":
    unittest.main(verbosity=2)
