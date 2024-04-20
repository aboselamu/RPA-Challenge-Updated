from RPA.Browser.Selenium import Selenium 
import re
import time
import requests
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
# from browser_manager import BrowserManager as br
from classes.data_processor import DataProcessor


class DataRetriever:

    def __init__(self, browser_manager):
        self.browser_manager = browser_manager
        
    def retrive_data(self, num_months_ago, search_phrase):
        self.nu_months_ago = num_months_ago
        self.search_phrase = search_phrase
        
        # self.browser_manager = browser_manager
        dp = DataProcessor()
        
        browser = self.browser_manager.browser
        counter = 1
        
        # Handling the possible inputs
        if num_months_ago <= 0:
            num_months_ago =1
            
        # To compare the date
        current_date = datetime.now()
        target_date = current_date - timedelta(days=num_months_ago * 30)  # Assuming each month has 30 days)
    
        # to store articles for extraction
        articles_titiles = []    
        try:
            # browser.wait_until_element_is_visible("xpath://*[@id='main-content-area']/div[2]/div[2]", timeout=10)
            # Wait for the element to be visible with a timeout
            browser.wait_until_element_is_visible('css:.search-result__list', timeout=timedelta(seconds=10))
        except Exception as e:
            print(e, "NOOOOOO")
    
            # to handle paggination
        is_there_ShowMore = True
            
        while is_there_ShowMore:
            print("Inside while loop")
            # Search result section
            search_list_selector = browser.find_element(locator="css:.search-result__list")     
            #browser.find_element("xpath=//*[@id='main-content-area']/div[2]/div[2]")
            articles = browser.find_elements("tag:article", parent=search_list_selector)

            # the show more button
            button_locator = browser.find_elements("tag:button", parent=search_list_selector)

            # for each articles 
            for article in articles:
                print("inside article for loop") 
                # getting excert section
                excert = browser.find_element("tag:p",parent=article)
                print("after excert")
                # getting time and description of the post from excert
                time_of_post, description  = dp.extract_before_ellipsis(excert.text)
                print(time_of_post, description, "check here")
                try:
                    article_date = dp.formated_article_date(time_of_post)
                except Exception as e:
                    print(e, "article, date format")
                print("after article date")
                # check if the artices does contains date
                # if(article_date == None):
                #     continue
                try:

                    # checking the article date is in the time period of the input
                    if dp.is_within_time_frame(article_date, target_date):
                        title= browser.find_element("tag:h3", parent=article)
                        if title.text not in articles_titiles:
                            articles_titiles.append(title.text)
                            
                            # does the title or description contains money
                            # checking how many times the search keyword apears in title and description
                            no_of_search_phrase, contains = dp.no_of_topic_and_money_amount(title.text, 
                                                                                          description, 
                                                                                          search_phrase)
                            # finding the imgae of each article
                            image = browser.find_element(locator="tag:img", parent=article)
                            image_url = image.get_attribute('src')
    
                            picture_name = image_url.split("/")[-1]  # Extracting picture name from URL
                            output_path = Path(get_output_dir()) / picture_name
    
                            ready_article = {"No":counter, "Title": title.text, "Date": article_date, 
                                             "Description": description, "PictureFilename": picture_name, 
                                             "Count": no_of_search_phrase, "ContainsMoney": contains
                                                }
    
                            # Making work items to be saved on file
                            # for article in articles:
                            workitems.outputs.create(payload=ready_article)
                            print("work item created")

    
    
                            # data.append([counter,title.text, article_date, description, 
                            #                     picture_name, no_of_search_phrase, contains])
                            #update counter
                            counter+=1
    
                except Exception as e:
                    print(e, "try to put everything")
    
            # try to locate and close the ads section
            try:
                ads_locator = browser.find_element("xpath=//button[@aria-label='Close Ad']")
                browser.click_button(ads_locator) 
    
            except Exception as e:
                print("no ads locarion")
                pass
            
            # Trying to find if there is more article
            try: 
                # Scroll the element into view the show more button
                browser.scroll_element_into_view(button_locator)
                browser.wait_until_element_is_enabled(button_locator, timeout=10)
    
    
                browser.click_button(button_locator)
                time.sleep(5)
                print("Botton Clicked")
        
            except Exception as e: 
                is_there_ShowMore = False
                print("no button clicked")
                pass


