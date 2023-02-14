from bs4 import BeautifulSoup
import requests
import datetime
from pytz import timezone

class DailyWeather:
    def __init__(self):
        self.exists = False
        self.highTemp = -999
        self.lowTemp = 999
        self.avgTemp = 0
        self.avgTempCount = 0
        self.precipExists = False
        self.precipTotal = 0
        self.temps = []

    
    def update(self, temp, precipTotal):
        self.exists = True
        
        if temp > self.highTemp:
            self.highTemp = temp
        if temp < self.lowTemp:
            self.lowTemp = temp
        
        self.avgTemp = ((self.avgTemp * self.avgTempCount) + temp) / (self.avgTempCount + 1)
        self.avgTempCount += 1
        self.temps.append(temp)
        if(precipTotal):
            if self.precipExists:
                print(self)
                print("double precip total")
                
            self.precipExists = True
            self.precipTotal = precipTotal
        
data = []
for i in range(20000):
    data.append(DailyWeather())

epoch = datetime.datetime.fromtimestamp(0, datetime.timezone.utc)
east = timezone("US/Eastern")

def addData(d):
    #takes in a dict containing weather info
    day = datetime.datetime.fromtimestamp(int(d["valid_time_gmt"]), datetime.timezone.utc)
    day = day.astimezone(east)

    days = (day - epoch).days

    data[days].update(d["temp"], d["precip_total"])
    

def parseRequest(url):
    values = requests.get(url)
    values = values.text.replace("null", "None")
    d = eval(values)
    observations = d["observations"]
    for observation in observations:
        addData(observation)

        
def main():
    pass
