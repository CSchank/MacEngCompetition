#import FarmingController
from random import random
import matplotlib.pyplot as plt
import PID
from IrrigateNode import IrrigateNode

def updateMoisture(moisture,flow,rain):
    lossPerHour = 0.02 + random() * 0.01
    moisture = moisture + (- lossPerHour + flow + rain) / 60
    return moisture if moisture > 0 else 0

def updateFlow(flow):
    randomDev = 0.1
    flow = flow + (random() - 0.5) * randomDev
    return flow if flow > 0 else 0

def determineRain(oldRain):
    if oldRain == 0:
        rain = 0.1 if random() > 0.98 else 0
    else:
        rain = 0.1 if random() > 0.1 else 0
    return rain

def runSimulation(mins,simSpeed):
    irgNodes = [IrrigateNode(i, "Corn", 0, 0.5, 0.8, 10, 20, 1, 0) for i in range(5)]
    nodes = [(0.2, 0, 0), (0.5, 0, 0), (0.1, 0, 0)]
    history = []
    for i in range(mins):
        moisture, flow, rain = nodes[0]
        newRain = determineRain(rain)
        #controller = FarmingController(numberNodes = 2)
        for i, node in enumerate(nodes):
            moisture, flow, rain = node # old value for moisture
            reqFlow, error = irgNodes[i].operate(rain,moisture,flow)    #use the PID
            if error == 1:
                print("Flow requested not output for node %d" % i)
            elif error == 2:
                print("Max moisture exceeded on node %d" % i)
            elif error == 3:
                print("Currently raining on node %d" % i)
            elif error == 4:
                print("Max daily water exceeded on node %d" % i)
            nodes[i] = (updateMoisture(moisture,reqFlow,rain), updateFlow(reqFlow), newRain)
        history += [nodes[:]]
    return history

def outputGraph(nodeHistory):
    fig, (ax1,ax2,ax3) = plt.subplots(1,3,figsize=(15,6))
    colours = [(0.3,0.6,0.1),"b","r","k"]
    for i, timestep in enumerate(nodeHistory):
        for j, node in enumerate(timestep):
            moisture, flow, rain = node
            ax1.scatter(i, moisture, c=colours[j],s=0.5)
            ax2.scatter(i, flow, c=colours[j], s=0.5)
            ax3.scatter(i, rain, c=colours[j], s=0.5)
    ax1.set_xlabel("Time (minutes)")
    ax1.set_ylabel("Moisture content of soil")
    ax2.set_xlabel("Time (minutes)")
    ax2.set_ylabel("Flow rate (mm/m^2 equivalent)")
    ax3.set_xlabel("Time (minutes)")
    ax3.set_ylabel("Rain (mm/m^2/timestep)")
    plt.show()


history = runSimulation(4800,0)
outputGraph(history)