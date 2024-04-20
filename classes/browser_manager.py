from RPA.Browser.Selenium import Selenium 
import logging
from pathlib import Path
from robocorp import vault
from robocorp import excel
from robocorp import storage
from datetime import datetime
from robocorp.tasks import task
from robocorp import workitems
# from robocorp.workitems import WorkItems
from datetime import datetime, timedelta
from robocorp.tasks import get_output_dir

class BrowserManager:
    def __init__(self):
        self.browser = None

    #oppening the site aljazeera.com

    def opening_the_news_Site(self, url):

        # logger.info("Opening the news site.")
        self.browser = Selenium(auto_close = False)
        
        # Define Chrome options to disable popup blocking
        options = [
            "--disable-popup-blocking",
            "--ignore-certificate-errors"
        ]

        

        # Open browser with specified options
        self.browser.open_available_browser(url, 
                                            browser_selection="Chrome", 
                                            options=options)
        # browser.close_all_browsers()
        # return browser
        print("oppend browser at last")

    @task
    def search_the_phrase(self, phrase):
        self.phrase = phrase
        print("inside search method")
        if(self.browser):
            print("found browser")
        else:
            print("not found browser")
        # logger.info(f"Searching the phrase: {phrase}")
        # if the site contains collecting cookies 
        try:
            print("inside tyr")
            self.browser.click_button('Allow all')
            print("it clicked allow")

        except:
            print("it didn't clicked allow")
            pass
        # finding the serach icon and field
        locator1 = "//button[@aria-pressed='false']//*[name()='svg']"
        self.browser.wait_until_page_contains_element(locator1, timeout=10)
        self.browser.click_element(locator1)

        # inserting the search phrase in the input field
        self.browser.input_text("//input[@placeholder='Search']",phrase)
        self.browser.click_button("//button[@aria-label='Search Al Jazeera']")
        # self.browser.close_all_browsers()


        # Trying to find it there is a realated articles with the search phrase
        try:
            locator2 = "//select[@id='search-sort-option']"
            self.browser.wait_until_element_is_visible(locator2, timeout=10)
            self.browser.click_element(locator2)
            print("finding the search area")
        except Exception as e:
            print(e, ": No news associated with the search phrase")
        # sort by time
        dropdown_locator = "//select[@id='search-sort-option']/option[1]" 
        self.browser.click_element(dropdown_locator)
        print("completed opening and searching")
