import asyncio
import time
from selenium.webdriver.common.by import By
from copy import deepcopy
from get_hw_submissions import fetch_hw_submissions
from selenium_utils import wait_for_XPATH

XPATH_HW_latency = '//div[@class="table-responsive"]/table//tr[3]/td'
XPATH_HW_latest_change = '//div[@class="table-responsive"]/table//tr[4]/td'
XPATH_HW_deadline = '//div[@class="activity-information"]/div/div'


def fetch_HW_data(driver, HW_url, HW_name):
    # html_data = await fetch_page_content(HW_url)
    # print(HW_name, HW_url)
    driver.get(HW_url)
    time.sleep(2)
    wait_for_XPATH(driver, XPATH_HW_latency)
    HW_latency = driver.find_element(By.XPATH, XPATH_HW_latency).text
    HW_latest_change = driver.find_element(By.XPATH, XPATH_HW_latest_change).text
    wait_for_XPATH(driver, XPATH_HW_deadline)
    HW_deadline = driver.find_elements(By.XPATH, XPATH_HW_deadline)[-1].text
    HW_deadline = HW_deadline.replace("مهلت:", "").strip()
    
    submissions_url = HW_url + "&action=grading"
    HW_json = {
        "HW_url": HW_url,
        "HW_name": HW_name,
        "HW_latency": HW_latency,
        "HW_latest_change": HW_latest_change,
        "HW_deadline": HW_deadline
    }
    submissions = fetch_hw_submissions(driver, submissions_url, HW_json)
    HW_json["HW_submissions"] = submissions
    return HW_json