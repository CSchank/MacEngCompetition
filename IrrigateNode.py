import PID
import math

class IrrigateNode:
    def __init__(self,number, name, startTime, minMoist, maxMoist, minWater, maxWater, maxFlow,moisture):
        self.number = number
        self.name = name
        self.startTime = startTime
        self.minMoist = minMoist
        self.maxMoist = maxMoist
        #all in mm rain equiv per node.
        self.minWater = minWater
        self.maxWater = maxWater
        self.maxFlow = maxFlow

        self.moisture = moisture
        self.currentTime = 0
        self.sendFlow = 0.0
        self.overFlow = 0.0
        self.rainfall = 0.0
        self.water = 0.0
        self.pid = PID.PID()
        self.pid.update(moisture)
        self.pid.setPoint(minMoist)
        self.flush = False

#Send Data
    def getMinMoist(self,x):
        return self.minMoist
    def getMaxMoist(self,x):
        return self.maxMoist
    def getMinWater(self,x):
        return self.minWater
    def getMaxWater(self,x):
        return self.maxWater
    def getMaxFlow(self,x):
        return self.maxFlow
    def receiveFlow(self,x):
        return self.sendFlow
#Recieve Data
    def changeMinMoist(self,x):
        self.minMoist = x
    def changeMaxMoist(self,x):
        self.maxMoist = x
    def changeMinWater(self,x):
        self.minWater = x
    def changeMaxWater(self,x):
        self.maxWater = x
    def changeMaxFlow(self,x):
        self.maxFlow = x

#Operate
    def operate(self,rainfall,moisture,actualFlow):
        self.currentTime += 1
        self.moisture = moisture

        self.water += actualFlow
        if (self.currentTime  == (2400)):
            self.currentTime = 0

        if (self.flush and (abs(self.water - self.maxFlow) < 0.01)):
            self.endFlush()

        if ((self.currentTime == self.startTime - 300) or self.currentTime -2100 == self.startTime):
            if (self.water < self.maxWater):
                self.endDay()

        if (self.currentTime == self.startTime):
            self.water = 0
            if (self.flush):
                self.endFlush()
            if (self.water >= self.maxWater):
                return(0,4)

        if (rainfall > 0.01):
            return (0,3)
        if (abs(actualFlow - self.sendFlow) > 0.02):
            return (0,1)
        if (moisture > self.maxMoist):
            return (0,2)
        
        delta = self.pid.update(self.moisture)
        if (delta > self.maxFlow):
            delta = self.maxFlow
        elif (delta < 0):
            delta = 0
        return(delta,0)

    def endDay(self):
        self.pid.setPoint(self.maxMoist)
        self.flush = True

    def endFlush(self):
        self.pid.setPoint(self.minMoist)
        self.flush = False


