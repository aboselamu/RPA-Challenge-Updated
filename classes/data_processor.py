
import re
import time
import requests
import logging
from pathlib import Path

from datetime import datetime

from datetime import datetime, timedelta
from robocorp.tasks import get_output_dir

class DataProcessor:
    def __init__(self):
        pass

    # getting the date and description from the excert of the article
    def extract_before_ellipsis(self, text):
        print("INside extract_before_ecli")
        # checking if the text contains the excert
        if len(text) <=0:
            print("extract text len 0")
            return 
            
        # Split the text at '...'
        date_part = ""
        description_part = ""
        try:
            parts = text.split(" ...")
            # Take the first part, before the '...'
            date_part = parts[0]
            description_part=parts[1]
        except Exception as e:
            print(e)
            pass
        description_part.replace("Â","")
    
        return date_part, description_part
    
    # formating the article's date
    def formated_article_date(self, date_extracted):
        print("inside formated_ articl")
        # cleaning the date part
        date_extracted = date_extracted.strip()
        print(date_extracted, "heee")
        # Defining possible hours, minutes and seconds 
        possible_hms = ["second", "seconds","min\xadutes", 
                            "minute", "minutes", "hour","hours"]
        print(possible_hms)
        possible_days = ["day", "days"]
    
        possible_months_format_One =["January", "Feburary", "March", "April", 
                                        "May", "June", "July", "August", "September", 
                                        "October", "November", "December"]
    
        possible_months_format_Two =["Jan", "Feb", "Mar", "Apr",
                                        "May", "Jun", "Jul", "Aug", 
                                        "Sep", "Oct", "Nov", "Dec"]
       
        current_date = datetime.now()
       
        # Formatting the date to make it more easy to compare and returning the article times
        try:   
            if(date_extracted.split(" ")[1]) in possible_hms:
                date_object = current_date
                formatted_date = date_object.strftime("%Y%m%d")
                return formatted_date
            elif date_extracted.split(" ")[1] in possible_days:
                # Split the expression to extract the number of days
                num_days = int(date_extracted.split()[0])
                # Calculate the target date by subtracting the number of days from the current date
                date_object = current_date - timedelta(days=num_days)
                formatted_date = date_object.strftime("%Y%m%d")
    
                return formatted_date
    
            elif date_extracted.split(" ")[0] in possible_months_format_One:
                # Convert the date string to a datetime object
                date_object = datetime.strptime(date_extracted, "%B %d, %Y")
        
                # Format the datetime object to the desired format
                formatted_date = date_object.strftime("%Y%m%d")
        
                return formatted_date
    
            elif date_extracted.split(" ")[0] in possible_months_format_Two:
                # Convert the date string to a datetime object
                date_object = datetime.strptime(date_extracted, "%b %d, %Y")
                formatted_date= date_object.strftime("%Y%m%d")
                return formatted_date
            else:
                print("INside try")
                return None
    
        except Exception as e:
            print(e, "possible date format is not found")
            return None
    
    # comparing if the article time is with in the date of given period of time
    def is_within_time_frame(self, article_date, target_date):
    
        # Convert article date string to a datetime object
        try:
            article_datetime = datetime.strptime(article_date, "%Y%m%d")
        except Exception as e:
            return e, False
        
        # Check if the article date is within the time frame (since the target date)
        return article_datetime  >= target_date
    
    # checking if the topics and description contains money 
    # and how many times the title and description contains the search phrase
    def no_of_topic_and_money_amount(self, title, description, search_phrase):
    
        # Trying to find the number of times the title and description contains
        countT = title.split(" ").count(search_phrase)
        countD = description.split(" ").count(search_phrase)
    
        # Regex pattern to match various money formats
        pattern = r"\$\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?|\d+\s(?:dollars|USD)"
        
        # Find all matches in the text
        matchesT = re.findall(pattern, title)
        matchesD = re.findall(pattern, description)
    
        # returning the number of times money appears and if there is search phrase in both
        return countT + countD,  bool(matchesT + matchesD)
