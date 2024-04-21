"""
This module compute the extracted date
It interacts with data retriever and it will process data according to the give parameters
"""
import re
import logging
from datetime import datetime, timedelta
from config.logging_config import setup_logging

# Configure logging for this script
setup_logging()


class DataProcessor:
    """
    It handless the cleaning part of the extracted data
    It compares, evalute, and decide which data has to be saved
    """

    def __init__(self):
        pass

    def extract_before_ellipsis(self, text):
        """
        It will extract date and description from the excert of articles
        """

        # checking if the text contains the excert
        if len(text) <= 0:
            logging.info("There is no excert to process")
            return

        # Split the text at '...'
        date_part = ""
        description_part = ""
        try:
            parts = text.split(" ...")
            # Take the first part, before the '...'
            date_part = parts[0]
            description_part = parts[1]

        except Exception as e:
            logging.error('Unable to extract date from the excert: %s', e)

        # Futher cleaning the text
        description_part.replace("Â", "")

        return date_part, description_part

    def formated_article_date(self, date_extracted):
        """
        Formatting Date of the articles using the possible styles 
        """

        # cleaning the date part
        date_extracted = date_extracted.strip()

        # Defining possible hours, minutes and seconds
        possible_hms = ["second", "seconds", "min\xadutes",
                        "minute", "minutes", "hour", "hours"
                        ]

        possible_days = ["day", "days"]

        possible_months_format_one = ["January", "Feburary", "March",
                                      "April", "May", "June", "July",
                                      "August", "September", "October",
                                      "November", "December"
                                      ]

        possible_months_format_two = ["Jan", "Feb", "Mar", "Apr",
                                      "May", "Jun", "Jul", "Aug",
                                      "Sep", "Oct", "Nov", "Dec"
                                      ]

        current_date = datetime.now()

        # Formatting the date to make it more easy to compare and returning the article times
        try:
            if date_extracted.split(" ")[1] in possible_hms:
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

            elif date_extracted.split(" ")[0] in possible_months_format_one:
                # Convert the date string to a datetime object
                date_object = datetime.strptime(date_extracted, "%B %d, %Y")

                # Format the datetime object to the desired format
                formatted_date = date_object.strftime("%Y%m%d")

                return formatted_date

            elif date_extracted.split(" ")[0] in possible_months_format_two:
                # Convert the date string to a datetime object
                date_object = datetime.strptime(date_extracted, "%b %d, %Y")
                formatted_date = date_object.strftime("%Y%m%d")
                return formatted_date
            else:
                return None

        except Exception as e:
            logging.error('The article Date is not known: %s', e)
            return None

    def is_within_time_frame(self, article_date, target_date):
        """
        Compare the article time of post to the time required
        Returns only the article date that is with in time frame
        """
        # Convert article date string to a datetime object
        try:
            article_datetime = datetime.strptime(article_date, "%Y%m%d")
        except:
            return False

        # Check if the article date is within the time frame (since the target date)
        return article_datetime >= target_date

    def no_of_topic_and_money_amount(self, title, description, search_phrase):
        """
        Check if the topics and description contains money
        And how many times the title and description contains the search phrase
        """

        # Trying to find the number of times the title and description contains
        count_in_title = title.split(" ").count(search_phrase)
        count_in_description = description.split(" ").count(search_phrase)

        # Regex pattern to match various money formats
        pattern = r"\$\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?|\d+\s(?:dollars|USD)"

        # Find all matches in the text
        matches_title = re.findall(pattern, title)
        matches_description = re.findall(pattern, description)

        # returning the number of times money appears and if there is search phrase in both
        return count_in_title + count_in_description,  bool(matches_title + matches_description)
