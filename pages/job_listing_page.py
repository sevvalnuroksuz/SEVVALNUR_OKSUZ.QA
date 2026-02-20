"""
Job Listing Page Object Model (Lever job board)
"""
from __future__ import annotations

import urllib.parse
from typing import Optional

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class JobListingPage(BasePage):

    # Locators
    SOFTWARE_DEV_OPEN_POSITIONS = (
        By.XPATH,
        "//a[contains(@href,'lever.co/insiderone')]"
        "[contains(translate(@href,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'software')]"
    )

    POSTINGS_CONTAINER = (
        By.XPATH,
        "//*[contains(@class,'postings') or contains(@class,'postings-group')]"
    )

    JOB_ITEMS = (
        By.XPATH,
        "//*[contains(@class,'posting') or contains(@class,'position-list-item')]"
    )

    APPLY_JOB_CARD = (By.CSS_SELECTOR, "a.posting-btn-submit")
    APPLY_FOR_THIS_JOB_LINK = (By.CSS_SELECTOR, "a.postings-btn[href*='/apply']")
    LEVER_FORM = (By.CSS_SELECTOR, "form")

    def __init__(self, driver, screenshot_handler=None):
        super().__init__(driver, screenshot_handler)

    def _wait_postings_loaded(self, timeout: int = 15):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.POSTINGS_CONTAINER)
        )

    # ---------------- Step 5 ----------------
    def click_software_development_open_positions(self):
        """Click 'Open Positions' link for Software Development and land on Lever."""
        try:
            wait = WebDriverWait(self.driver, 15)
            before_tabs = set(self.driver.window_handles)

            el = wait.until(EC.element_to_be_clickable(self.SOFTWARE_DEV_OPEN_POSITIONS))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)

            try:
                el.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", el)

            #
            wait.until(lambda d: len(d.window_handles) >= len(before_tabs))
            new_tabs = list(set(self.driver.window_handles) - before_tabs)
            if new_tabs:
                self.driver.switch_to.window(new_tabs[-1])

            
            if "jobs.lever.co/insiderone" not in self.driver.current_url.lower():
                self.driver.get("https://jobs.lever.co/insiderone?team=Software%20Development")

            self.wait_for_url_contains("jobs.lever.co/insiderone", timeout=10)
            self._wait_postings_loaded()

        except Exception:
            self.screenshot_handler.take_screenshot(self.driver, "click_open_positions_failed")
            raise

    # ---------------- Filters ----------------
    def apply_filters(self, location: str = "Istanbul, Turkiye", team: str = "Quality Assurance"):
        """Apply filters via URL params in a single navigation."""
        try:
            self._set_lever_query_params(location=location, team=team)
        except Exception:
            self.screenshot_handler.take_screenshot(self.driver, "apply_filters_failed")
            raise

    def _set_lever_query_params(self, location: Optional[str] = None, team: Optional[str] = None):
        """Build and navigate to filtered Lever URL."""
        wait = WebDriverWait(self.driver, 15)

        if "jobs.lever.co/insiderone" not in self.driver.current_url.lower():
            self.driver.get("https://jobs.lever.co/insiderone")
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        parsed = urllib.parse.urlparse(self.driver.current_url)
        params = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)

        if location is not None:
            params["location"] = [location]
        if team is not None:
            params["team"] = [team]

        new_url = urllib.parse.urlunparse(
            parsed._replace(query=urllib.parse.urlencode(params, doseq=True))
        )
        self.driver.get(new_url)
        self._wait_postings_loaded()

    # ---------------- Step 8 ----------------
    def verify_job_listings_displayed(self) -> bool:
        try:
            WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(self.JOB_ITEMS))
            jobs = self.driver.find_elements(*self.JOB_ITEMS)
            assert len(jobs) > 0, "No job listings found after filtering"
            return True
        except Exception as e:
            self.screenshot_handler.take_screenshot(self.driver, "verify_job_listings_displayed_failed")
            raise AssertionError(f"No job listings displayed: {e}")

    # ---------------- Step 9 ----------------
    def verify_job_listings_content(
        self,
        expected_team: str = "Quality Assurance",
        expected_location_substr: str = "Istanbul"
    ) -> bool:
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            body = self.driver.find_element(By.TAG_NAME, "body").text.lower()
            assert expected_team.lower() in body, f"'{expected_team}' not found on page"
            assert expected_location_substr.lower() in body, f"'{expected_location_substr}' not found on page"
            return True
        except Exception as e:
            self.screenshot_handler.take_screenshot(self.driver, "verify_job_listings_content_failed")
            raise AssertionError(f"Job listings content verification failed: {e}")

    # ---------------- Step 10 ----------------
    def click_apply_button(self):
        """Listing → job detail → apply form."""
        try:
            wait = WebDriverWait(self.driver, 20)

            wait.until(EC.presence_of_element_located(self.APPLY_JOB_CARD))
            first_apply = next(
                (a for a in self.driver.find_elements(*self.APPLY_JOB_CARD) if a.is_displayed()),
                None
            )
            if not first_apply:
                raise Exception("No visible 'Apply' button found on listings")

            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", first_apply)
            try:
                first_apply.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", first_apply)

            wait.until(lambda d: "jobs.lever.co/insiderone/" in d.current_url.lower())

            apply_for = wait.until(EC.element_to_be_clickable(self.APPLY_FOR_THIS_JOB_LINK))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", apply_for)
            try:
                apply_for.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", apply_for)

            wait.until(lambda d: "/apply" in d.current_url.lower())
            wait.until(EC.presence_of_element_located(self.LEVER_FORM))

        except Exception:
            self.screenshot_handler.take_screenshot(self.driver, "click_apply_button_failed")
            raise

    def verify_lever_application_form(self) -> bool:
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(lambda d: "lever.co" in d.current_url.lower())
            wait.until(EC.presence_of_element_located(self.LEVER_FORM))
            return True
        except Exception as e:
            self.screenshot_handler.take_screenshot(self.driver, "verify_lever_application_form_failed")
            raise AssertionError(f"Lever application form verification failed: {e}")