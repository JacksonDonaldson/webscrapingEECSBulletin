from bs4 import BeautifulSoup
from selenium import webdriver


import re

import time
def getSoup(url: str) -> BeautifulSoup:
    
    with webdriver.Chrome() as driver:
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(3)
        bs = BeautifulSoup(driver.page_source, "html.parser")
    
    return bs

soup = getSoup("https://bulletin.engin.umich.edu/courses/eecs/")

courses = soup.findAll("strong")
courses = [c for c in courses if "EECS" in str(c)]
