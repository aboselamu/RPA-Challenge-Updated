"""
This module act as producer for the work items.
It produces tons of payload depending on the search result
"""
import logging
from robocorp import vault
from robocorp import storage
from robocorp.tasks import task
from classes.browser_manager import BrowserManager as BM
from classes.data_retriever import DataRetriever
from config.logging_config import setup_logging

# Configure logging for this script
setup_logging()


@task
def main():
    """ 
    This function starts the tasks and it calls all the methods from the necessary pakay and class.
    It also produces work loads
    """

    logging.info("Starting the Robot...")

    # getting the website
    secrets = vault.get_secret('alijazeersite')

    # Retrieve the text content from the asset
    content = storage.get_text("parameters")

    # splitting it to search phrase and number of months
    search_phrase, number_of_months = content.split(',')

    # Convert number_of_months to an integer
    number_of_months = int(number_of_months.strip())

    # Performing cleaning the phrase
    search_phrase = search_phrase.strip()

    # creating instance of Browser Manager Class
    bm = BM()
    bm.opening_the_news_Site(secrets["url"])
    bm.search_the_phrase(search_phrase)

    # creating instance of Data Retriever Class
    dr = DataRetriever(bm)
    dr.retrive_data(number_of_months, search_phrase)


# def close_the_browser():
#     global bm
    # Close the browser
    # bm.close_browser()
