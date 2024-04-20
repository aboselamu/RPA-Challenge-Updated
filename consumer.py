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

@task
def save_data_to_Excel():

    # Define the path for the new Excel file in the output directory
    output_dir = Path(get_output_dir())
    excel_file_path = output_dir / "Articles.xlsx"
    
    # Create a new Excel workbook and add a worksheet with the name 'Sheet1'
    workbook = excel.create_workbook(fmt="xlsx", sheet_name="Sheet1")
    
    
    # Append a row with column headers
    sheet_name = "Sheet1"
    worksheet = workbook.worksheet(sheet_name)
    row_to_append = [
        ["No", "Title", "Date", "Description", "PictureFilename", "Count", "ContainsMoney"]
    ]
    # Append the row to the worksheet
    worksheet.append_rows_to_worksheet(row_to_append, header=False)
    
    # worksheet = workbook.worksheet(sheet_name)
    workbook.save(excel_file_path)
    headers = ["No", "Title", "Date", "Description", "PictureFilename", "Count", "ContainsMoney"]
    print("inside save to excel function")
    try:
        # Fetch the created work items and write them to the Excel file
        for item in workitems.inputs:
            row = [
                item.payload.get("No", ""),
                item.payload.get("Title", ""),
                item.payload.get("Date", ""),
                item.payload.get("Description", ""),
                item.payload.get("PictureFilename", ""),
                item.payload.get("Count", ""),
                item.payload.get("ContainsMoney", "")
            ]
            worksheet.append_rows_to_worksheet([row], header=False)
        workbook.save(excel_file_path)
        print("workitems finished successfully")
    except Exception as e:
        print(e, "save item didn't work")
        pass
