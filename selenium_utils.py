from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import aiohttp

def wait_for_XPATH(driver, xpath, delay=5):
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return myElem
    except TimeoutException:
        print ("Loading took too much time!")


def wait_for_ID(driver, ID, delay=5):
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, ID)))
        return myElem
    except TimeoutException:
        print ("Loading took too much time!")