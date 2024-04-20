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
from class.data_processor import DataProcessor


class DataRetriever:

    def __init__(self, browser_manager):
        self.browser_manager = browser_manager
    def retrive_data(self, num_months_ago, search_phrase):
        self.nu_months_ago = num_months_ago
        self.search_phrase = search_phrase
        # self.browser_manager = browser_manager
        dp = DataProcessor()

        browser = self.browser_manager.browser
        # browser = browser_manager
        # Declearing varibale to return the date
        # data =[]
        counter = 1
        # Handling the possible inputs
        if num_months_ago == 0:
            num_months_ago =1
        # To compare the date
        current_date = datetime.now()
        target_date = current_date - timedelta(days=num_months_ago * 30)  # Assuming each month has 30 days)
    
        # to store articles for extraction
        articles_titiles = []    
        try:
            browser.wait_until_element_is_visible("xpath://*[@id='main-content-area']/div[2]/div[2]", timeout=10)
        except Exception as e:
            print(e, "NOOOOOO")
    
            # to handle paggination
        is_there_ShowMore = True
            
        while is_there_ShowMore:
            print("Inside while loop")
            # Search result section
            search_list_selector = browser.find_element("xpath=//*[@id='main-content-area']/div[2]/div[2]")
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
                                             "Description": description, "Picture Filename": picture_name, 
                                             "Count": no_of_search_phrase, "Contains Money": contains
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

    # # getting the date and description from the excert of the article
    # def extract_before_ellipsis(self, text):
    #     print("INside extract_before_ecli")
    #     # checking if the text contains the excert
    #     if len(text) <=0:
    #         print("extract text len 0")
    #         return 
            
    #     # Split the text at '...'
    #     date_part = ""
    #     description_part = ""
    #     try:
    #         parts = text.split(" ...")
    #         # Take the first part, before the '...'
    #         date_part = parts[0]
    #         description_part=parts[1]
    #     except Exception as e:
    #         print(e)
    #         pass
    #     description_part.replace("Â","")
    
    #     return date_part, description_part
    
    # # formating the article's date
    # def formated_article_date(self, date_extracted):
    #     print("inside formated_ articl")
    #     # cleaning the date part
    #     date_extracted = date_extracted.strip()
    #     print(date_extracted, "heee")
    #     # Defining possible hours, minutes and seconds 
    #     possible_hms = ["second", "seconds","min\xadutes", 
    #                         "minute", "minutes", "hour","hours"]
    #     print(possible_hms)
    #     possible_days = ["day", "days"]
    
    #     possible_months_format_One =["January", "Feburary", "March", "April", 
    #                                     "May", "June", "July", "August", "September", 
    #                                     "October", "November", "December"]
    
    #     possible_months_format_Two =["Jan", "Feb", "Mar", "Apr",
    #                                     "May", "Jun", "Jul", "Aug", 
    #                                     "Sep", "Oct", "Nov", "Dec"]
       
    #     current_date = datetime.now()
       
    #     # Formatting the date to make it more easy to compare and returning the article times
    #     try:   
    #         if(date_extracted.split(" ")[1]) in possible_hms:
    #             date_object = current_date
    #             formatted_date = date_object.strftime("%Y%m%d")
    #             return formatted_date
    #         elif date_extracted.split(" ")[1] in possible_days:
    #             # Split the expression to extract the number of days
    #             num_days = int(date_extracted.split()[0])
    #             # Calculate the target date by subtracting the number of days from the current date
    #             date_object = current_date - timedelta(days=num_days)
    #             formatted_date = date_object.strftime("%Y%m%d")
    
    #             return formatted_date
    
    #         elif date_extracted.split(" ")[0] in possible_months_format_One:
    #             # Convert the date string to a datetime object
    #             date_object = datetime.strptime(date_extracted, "%B %d, %Y")
        
    #             # Format the datetime object to the desired format
    #             formatted_date = date_object.strftime("%Y%m%d")
        
    #             return formatted_date
    
    #         elif date_extracted.split(" ")[0] in possible_months_format_Two:
    #             # Convert the date string to a datetime object
    #             date_object = datetime.strptime(date_extracted, "%b %d, %Y")
    #             formatted_date= date_object.strftime("%Y%m%d")
    #             return formatted_date
    #         else:
    #             print("INside try")
    #             return None
    
    #     except Exception as e:
    #         print(e, "possible date format is not found")
    #         return None
    
    # # comparing if the article time is with in the date of given period of time
    # def is_within_time_frame(self, article_date, target_date):
    
    #     # Convert article date string to a datetime object
    #     try:
    #         article_datetime = datetime.strptime(article_date, "%Y%m%d")
    #     except Exception as e:
    #         return e, False
        
    #     # Check if the article date is within the time frame (since the target date)
    #     return article_datetime  >= target_date
    
    # # checking if the topics and description contains money 
    # # and how many times the title and description contains the search phrase
    # def no_of_topic_and_money_amount(self, title, description, search_phrase):
    
    #     # Trying to find the number of times the title and description contains
    #     countT = title.split(" ").count(search_phrase)
    #     countD = description.split(" ").count(search_phrase)
    
    #     # Regex pattern to match various money formats
    #     pattern = r"\$\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?|\d+\s(?:dollars|USD)"
        
    #     # Find all matches in the text
    #     matchesT = re.findall(pattern, title)
    #     matchesD = re.findall(pattern, description)
    
    #     # returning the number of times money appears and if there is search phrase in both
    #     return countT + countD,  bool(matchesT + matchesD)
