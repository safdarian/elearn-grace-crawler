from selenium.webdriver.common.by import By
from selenium_utils import wait_for_XPATH
import re

def get_class_url(driver, needed_class_name, needed_class_subtitle):
    
    # CLASS_URL_XPATH = '//div[contains(@class, "course-card")]/div[1]//a'
    CLASS_URL_XPATH = '//a[contains(@class, "coursename")]'
    CLASS_SUBTITLE_XPATH = '//a[contains(@class, "coursename")]/following-sibling::div'


    wait_for_XPATH(driver, CLASS_URL_XPATH)

    class_url_elements = driver.find_elements(By.XPATH, CLASS_URL_XPATH)
    class_subtitle_elements = driver.find_elements(By.XPATH, CLASS_SUBTITLE_XPATH)

    course_names = [class_url.text for class_url in class_url_elements]
    course_subtitles = [class_subtitle.text for class_subtitle in class_subtitle_elements]
    class_urls = [class_url.get_attribute("href") for class_url in class_url_elements]

    # print(course_names)


    # Find the index of the class we need using re.find needed_class_name in class_names
    needed_class_index = -1
    for i, class_name in enumerate(course_names):
        if re.search(needed_class_name, class_name):
            if re.search(needed_class_subtitle, course_subtitles[i]):
                needed_class_index = i
                break
    return class_urls[needed_class_index]