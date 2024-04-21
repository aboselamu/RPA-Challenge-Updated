"""
This module will open the site by configuring the browser
"""
import logging
from robocorp.tasks import task
from RPA.Browser.Selenium import Selenium
from config.logging_config import setup_logging

# Configure logging for this script
setup_logging()


class BrowserManager:
    """
    This will mange the browser and open it by using the options.
    """

    def __init__(self):
        self.browser = None

    def opening_the_news_site(self, url):
        """
        It will take one argument url and will configure the browser
        It will use Chrome to ope the site
        """
        logging.info("Opening Browser")

        # logger.info("Opening the news site.")
        self.browser = Selenium(auto_close=False)

        # Define Chrome options to disable popup blocking
        options = [
            "--disable-popup-blocking",
            "--ignore-certificate-errors"
        ]

        # Open browser with specified options
        self.browser.open_available_browser(url,
                                            browser_selection="Chrome",
                                            options=options)

        logging.info("Browser Opened Successfully:")

    @task
    def search_the_phrase(self, phrase):
        """
        This method takes one argument which is a search phrase related to specific topic
        It will manage the searching 
        It will manage the sorting
        """
        # self.phrase = phrase

        # if the site contains collecting cookies
        try:
            self.browser.click_button('Allow all')
        except:
            pass
        # finding the serach icon and field
        locator1 = "//button[@aria-pressed='false']//*[name()='svg']"
        self.browser.wait_until_page_contains_element(locator1, timeout=10)
        self.browser.click_element(locator1)

        try:

            # inserting the search phrase in the input field
            self.browser.input_text("//input[@placeholder='Search']", phrase)
            self.browser.click_button(
                "//button[@aria-label='Search Al Jazeera']")
            logging.info("Search Success")

        except Exception as e:
            logging.error('Unable to search the phrase, due to: %s', e)

        locator2 = "//select[@id='search-sort-option']"

        # Trying to find it there is a realated articles with the search phrase
        try:

            self.browser.wait_until_element_is_visible(locator2, timeout=10)
            self.browser.click_element(locator2)
            logging.info("There is articles related to the search phrase")

        except Exception as e:
            logging.error('No news associated with the phrase: %s', e)

        # sort by time
        try:
            dropdown_locator = "//select[@id='search-sort-option']/option[1]"
            self.browser.wait_until_page_contains_element(
                dropdown_locator, timeout=5)
            self.browser.click_element(dropdown_locator)
        except Exception as e:
            logging.error('Unable to sort the result by time: %s', e)
