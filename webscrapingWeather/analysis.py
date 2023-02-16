import pickle
from DailyWeather import DailyWeather
import os
import seaborn as sb
import matplotlib.pyplot as plt

def getTempDifferenceArray(days, data):
    difAr = [None] * len(data)
    for i in range(len(data)):
        if i - days >= 0:
            difAr[i] = abs(data[i].avgTemp - data[i - days].avgTemp)
    return difAr

def showDailyDifferencePlot(dayRange):

    days = []
    vals = []
    for i in range(dayRange):
        days.append(i)
        difs = getTempDifferenceArray(i, data)
        difs = [d for d in difs if d!= None]
        avg = sum(difs) / len(difs)
        vals.append(avg)
    plot = sb.scatterplot(x=days, y=vals)
    print(plot)
    plt.xlabel("Days Looked Back")
    plt.ylabel("Average difference in temperature")
    
    plt.show()

def showAvgTemperature():
    days = []
    vals = []
    for i in range(len(data)):
        days.append(i)
        vals.append(data[i].avgTemp)
    plot = sb.scatterplot(x=days, y=vals)
    plt.xlabel("Days since Jan 1 1970")
    plt.ylabel("Average Temperature")
    plt.show()
def analyze(data):
    #data: A collection of DailyWeather objects
    pass

    
def main():
    global data
    if(os.path.isfile("weather.dat")):
        
        print("Cached data found! Starting analysis...")

        data = pickle.load(open("weather.dat", "rb"))
        analyze(data)
    else:
        print("Cached data not found! Please use scrape.py to grab data.")
        

        
if __name__ == "__main__":
    main()
    
