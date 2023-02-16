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
        if temp == None:
            #print("None temp found")
            return
        
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
