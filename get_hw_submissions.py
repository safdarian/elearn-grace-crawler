import json
import os
from tqdm import tqdm
import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

from selenium_utils import wait_for_ID, wait_for_XPATH
from date_manager import parse_persian_date


def fetch_hw_submissions(driver, url, hw_data):
    # use in case of change in submissions url pattern
    # SCORE_BUTTON_XPATH = '//a[contains(@class, "btn-primary")]'
    # score_button = wait_for_XPATH(driver, SCORE_BUTTON_XPATH)
    # driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'nearest'});", score_button)
    # time.sleep(1)
    # score_button.click()
    # time.sleep(8)
    
    driver.get(url)
    ROW_XPATH = '//table[contains(@class, "generaltable")]/tbody/tr'
    while len(driver.find_elements(By.XPATH, ROW_XPATH)) == 0:
        driver.refresh()
        time.sleep(8)
        
    perpage_select_element = driver.find_elements(By.XPATH, '//select[@name="perpage"]')[0]
    perpage_select = Select(perpage_select_element)
    # print(perpage_select.options)
    perpage_select.select_by_visible_text("همه")
    time.sleep(5)

    wait_for_XPATH(driver, ROW_XPATH)

    rows = driver.find_elements(By.XPATH, ROW_XPATH)

    data = []
    for row in rows:
        columns = row.find_elements(By.XPATH, ".//td")
        name = columns[1].text
        name = name.split("\n")[-1]
        student_number = columns[2].text
        email = columns[3].text
        submission = columns[4].text
        last_change = columns[7].text
        last_change = last_change.split("\n")[-1]
        file_name_element = columns[12]
        
        if submission:
            submission_status = columns[4].find_elements(By.CLASS_NAME, "submissionstatussubmitted")[0].text if columns[4].find_elements(By.CLASS_NAME, "submissionstatussubmitted") else None
            submission_latency = columns[4].find_elements(By.CLASS_NAME, "latesubmission")[0].text if columns[4].find_elements(By.CLASS_NAME, "latesubmission") else None
            
            if not submission_status:
                submission_status = columns[4].find_elements(By.CLASS_NAME, "submissionstatus")[0].text if columns[4].find_elements(By.CLASS_NAME, "submissionstatus") else None
            

            file_divs = row.find_elements(By.XPATH, ".//div[@class='fileuploadsubmission']")
            if file_divs:
                file_div = file_divs[0]
                file_name = file_div.find_elements(By.XPATH, ".//img")[0].get_attribute("alt") if file_div.find_elements(By.XPATH, ".//img") else None
            else:
                file_div = None
                file_name = None
            # file_div = row.find_elements(By.XPATH, ".//td[contains(@class, 'ygtvcontent')]")[0]
            
            # print(file_name)
        
        data.append({
            "name": name,
            "student_number": student_number,
            "email": email,
            "last_change": last_change,
            "submission_status": submission_status,
            "submission_latency": submission_latency,
            "file_name": file_name,
            "last_change_parsed": parse_persian_date(last_change),
            "hw_name": hw_data["HW_name"]
        })


    
    
    HW_deadline = hw_data["HW_deadline"]
    HW_deadline_parsed = parse_persian_date(HW_deadline)

    for i in range(len(data)):
        data[i]["HW_deadline"] = HW_deadline
        data[i]["HW_deadline_parsed"] = HW_deadline_parsed
        condition = data[i]["last_change_parsed"] > HW_deadline_parsed if data[i]["last_change_parsed"] else False
        used_grace = data[i]["last_change_parsed"] - HW_deadline_parsed if condition else 0
        data[i]["used_grace"] = used_grace
    os.makedirs("output", exist_ok=True)
    pd.DataFrame(data).to_csv(f"output/{hw_data["HW_name"]}_submissions.csv", index=False, encoding="utf-8")
    return data