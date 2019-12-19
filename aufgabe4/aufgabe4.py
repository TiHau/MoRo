from Robot_Simulator_V3 import labyrinthWorld
from Robot_Simulator_V3 import Robot
from Robot_Simulator_V3 import sensorUtilities
import numpy as np
# from aufgabe3.aufgabe3_b import followLine

myWorld = labyrinthWorld.buildWorld()
myRobot = Robot.Robot()
myWorld.setRobot(myRobot, [2, 18, 0])

FOLLOW_RIGHT = True # False for left hand
SHOWLINES = "all" # left, alternate, none, all

myKeyboardController = myWorld.getKeyboardController()

alternate = True
while True:
    (motion,boxCmd,exit) = myKeyboardController.getCmd()
    if exit:
        break
    myRobot.move(motion)
    dists = myRobot.sense()
    directions = myRobot.getSensorDirections()
    line = sensorUtilities.extractSegmentsFromSensorData(dists[4:8], directions[4:8])

    crash_dist = 100
    if dists[13] and dists[14]:
        crash_dist = (dists[13]+dists[14])/2
    print(crash_dist)

    if len(line) > 0:
        line = line[0]
        print(line)

        offset = 1
        line = [[line[0][0], line[0][1] + offset], [line[1][0], line[1][1] + offset]]
        border_line = sensorUtilities.transformPolylinesL2G([line], myWorld.getTrueRobotPose())
        myWorld.drawPolylines(border_line, "light green")

myWorld.close(False)