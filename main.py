import asyncio
import os
from tqdm import tqdm
import jdatetime
from selenium import webdriver  
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import json
import pandas as pd
from selenium_utils import wait_for_ID, wait_for_XPATH
from course_list import get_class_url
from get_hw_data import fetch_HW_data
# from date_manager import parse_persian_date
import Levenshtein

def login(driver, USERNAME, PASSWORD):
    main_page_url = "https://elearn.ut.ac.ir/my/courses.php"

    driver.get(main_page_url)

    time.sleep(2)

    username = wait_for_ID(driver, "Username")
    password = wait_for_ID(driver, "password")
    login_button = wait_for_XPATH(driver, '//button[@type="submit"]')

    username.send_keys(USERNAME)
    password.send_keys(PASSWORD)
    login_button.click()

    time.sleep(2)


async def main():
    with open("login_credentials.json", "r") as config_file:
        config = json.load(config_file)
    with open("crawler_config.json", "r") as config_file:
        crawler_config = json.load(config_file)

    USERNAME = config["username"]
    PASSWORD = config["password"]
    COURSE_NAME = crawler_config["course_name"]
    COURSE_SUBTITLE = crawler_config["course_subtitle"]
    url = crawler_config.get("begin_url", "")
    HW_LIST = crawler_config["HW_list"]
    HW_NAME_THRESHOLD = crawler_config["HW_name_threshold"]
    HEADLESS = crawler_config["headless"]

    options = Options()
    
    if HEADLESS:
        options.add_argument("--headless")
    
    options.add_argument("--window-size=1920,1200")

    driver = webdriver.Chrome(options=options)
    
    login(driver, USERNAME, PASSWORD)

    class_url = get_class_url(driver, COURSE_NAME, COURSE_SUBTITLE)

    driver.get(class_url)

    time.sleep(2)

    HW_URL_XPATH = '//div[contains(@class, "assessment")]/following-sibling::div[1]//a'

    HW_elements = driver.find_elements(By.XPATH, HW_URL_XPATH)


    HW_names = []
    for HW_element in HW_elements:
        outer_span = HW_element.find_element(By.XPATH, './/span[@class="instancename"]')
        outer_span_text = driver.execute_script("return arguments[0].childNodes[0].nodeValue;", outer_span)
        HW_names.append(outer_span_text)


    HW_urls = [HW_element.get_attribute("href") for HW_element in HW_elements]

    HW_data = []
    for HW_name, HW_url in zip(HW_names, HW_urls):
        # if minimum edit distance between HW_name and HW_list is more than 1, skip this HW
        if all(Levenshtein.distance(HW_name, HW_name_list, weights=(1, 1, 1)) > HW_NAME_THRESHOLD for HW_name_list in HW_LIST):
            continue
        HW_json = fetch_HW_data(driver, HW_url, HW_name)
        HW_data.append(HW_json)
    all_submissions = []
    for HW in HW_data:
        all_submissions += HW["HW_submissions"]
    all_submissions = sorted(all_submissions, key=lambda x: (x["student_number"], x["HW_deadline_parsed"]))

    for i in range(0, len(all_submissions)):
        if i == 0 or all_submissions[i]["student_number"] != all_submissions[i - 1]["student_number"]:
            all_submissions[i]["total_grace"] = all_submissions[i]["used_grace"]
        else:
            if all_submissions[i]["used_grace"] == 0:
                all_submissions[i]["total_grace"] = all_submissions[i - 1]["total_grace"]
            elif all_submissions[i - 1]["total_grace"] == 0:
                all_submissions[i]["total_grace"] = all_submissions[i]["used_grace"]
            else:
                all_submissions[i]["total_grace"] = all_submissions[i - 1]["total_grace"] + all_submissions[i]["used_grace"]
            
    
    for i in range(len(all_submissions)):
        all_submissions[i]["used_grace"] = str(all_submissions[i]["used_grace"])
        all_submissions[i]["total_grace"] = str(all_submissions[i]["total_grace"])

    HW_df = pd.DataFrame(all_submissions)
    
    
    os.makedirs("output", exist_ok=True)
    HW_df.to_excel("output/HW_grace.xlsx")
    
    
    


if __name__ == "__main__":
    asyncio.run(main())
