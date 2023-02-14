from bs4 import BeautifulSoup
from selenium import webdriver
import re
import time
import os


def getSoup(url: str) -> BeautifulSoup:
    if(os.path.isfile("webdata.html")):
        s = open("webdata.html").read()
    else:
        
        with webdriver.Chrome() as driver:
            driver.get(url)
            time.sleep(3)
            s = driver.page_source
        with open("webdata.html", "w") as f:
            f.write(s)
            
            

    bs = BeautifulSoup(s, "html.parser")
    
    return bs

soup = getSoup("https://bulletin.engin.umich.edu/courses/eecs/")

courses = soup.findAll("strong")
courses = [c for c in courses if "EECS" in str(c)]

#grab prerequisite and course elements
courses = [(c, c.parent.find("em")) for c in courses]

courseDict = dict()

for c in courses:
    name = c[0]
    prereq = c[1]

    try:
        name = name.text[:name.text.index(".")]
        courseDict[name] = prereq.text
    except:
        #stupid eecs 410
        if "EECS 410" in courseDict:
            raise Exception("They added a second stupid course with name" + name.text)
        courseDict["EECS 410"] = prereq.text

interpretedCourses = dict()

for key in courseDict:
    prereq = courseDict[key]
    if "None" in prereq:
        print(prereq)
        interpretedCourses[key] = None
        courseDict[key] = None

for key in courseDict:
    if courseDict[key]:
        prereq = courseDict[key]
        prev = courseDict[key]
        courseDict[key] = re.sub('Minimum grade of “[a-zA-Z]” required for enforced prerequisites.', '', courseDict[key])
        courseDict[key] = re.sub('(\d credits?)', "", courseDict[key])
        courseDict[key] = re.sub("\\[Fewer .+\\]", "", courseDict[key]) #mildly iffy
        courseDict[key] = re.sub("[aA]dvisory [pP]rerequisite.*", "", courseDict[key])
        courseDict[key] = re.sub("Minimum .*\.", "", courseDict[key])
        courseDict[key] = re.sub("(minimum grade of “?[ABCDE]”?)", "", courseDict[key])
        courseDict[key] = re.sub("()", "", courseDict[key])
    
