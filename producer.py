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
from browser_manager import BrowserManager as BM 
from data_retriever import DataRetriever 

@task
def main():
    bm = BM()
    url = "https://www.aljazeera.com/"
    sp = "Business"
    number_of_months = 1
    bm.opening_the_news_Site(url)
    bm.search_the_phrase(sp)
    dr = DataRetriever(bm)
    dr.retrive_data(number_of_months, sp)
def close_the_browser():
    global bm
    # Close the browser
    # bm.close_browser()

# @task
# def producer():

    
    # Close the browser
    # bm.close_browser()


    # save_data_to_Excel(workbook, sheet_name)
    # workbook.save(excel_file_path)

    # Saving the workbook
    # workbook.save(excel_file_path)
    
