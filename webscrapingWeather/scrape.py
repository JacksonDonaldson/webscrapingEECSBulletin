from bs4 import BeautifulSoup
import requests
import datetime
from pytz import timezone
import asyncio
import httpx
import os
import pickle
from DailyWeather import DailyWeather


        
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
    

async def parseRequest(url, year):
    async with httpx.AsyncClient() as client:
        years[year] += 1
        values = await client.get(url)
        years[year] -=1
        values = values.text.replace("null", "None")
        d = eval(values)
        observations = d["observations"]
        for observation in observations:
            addData(observation)
    print("finished month in", year)
    #years[year] += 1
api = "https://api.weather.com/v1/location/KDTW:9:US/observations/historical.json?apiKey=e1f10a1e78da46f5b10a1e78da96f525&units=e&"

years = [0] * 2100

def getPaddedMonth(month):
    s = str(month)
    if len(s) == 1:
        s = "0" + s
    return s

from calendar import monthrange

async def grabData():
    tasks = []
    for year in range(1970, 2023):
        for month in range(1,13):
            #print(year)
            url = api + "startDate=" + str(year) + getPaddedMonth(month) + "01" + "&endDate=" + str(year) + getPaddedMonth(month) + str(monthrange(year, month)[1])
            tasks.append(asyncio.create_task(parseRequest(url, year)))

    done, pending = await asyncio.wait(tasks)
    print(done, pending)
    #print(year)


            
def main():
    global data
    if(os.path.isfile("weather.dat")):
        
        print("cached data already found...")

        data = pickle.load(open("weather.dat", "rb"))
    else:
        print("Cached data not found!\nGrabbing weather data...")
        asyncio.run(grabData())
        print("Data scraped. Please manually clean up the data array, then pickle it to weather.dat")
        exit()

    
        
if __name__ == "__main__":
    main()
