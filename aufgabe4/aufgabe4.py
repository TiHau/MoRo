from Robot_Simulator_V3 import labyrinthWorld
from Robot_Simulator_V3 import Robot
from Robot_Simulator_V3 import sensorUtilities
import numpy as np

myWorld = labyrinthWorld.buildWorld()
myRobot = Robot.Robot()
myWorld.setRobot(myRobot, [2, 18, 0])

FOLLOW_RIGHT = True # False for left hand
SHOWLINES = "right" # left, alternate, none, all

myKeyboardController = myWorld.getKeyboardController()

alternate = True
while True:
    (motion,boxCmd,exit) = myKeyboardController.getCmd()
    if exit:
        break
    myRobot.move(motion)
    dists = myRobot.sense()
    directions = myRobot.getSensorDirections()
    lines_l = sensorUtilities.extractSegmentsFromSensorData(dists, directions)
    
    left_list = []
    right_list = []
    if len(lines_l) > 1:
        for line in lines_l:
            if line[0][1] > 0 and line[1][1] > 0:
                left_list.append(line)
            else:
                right_list.append(line)
    
    #TODO get line that is the most parallel to the robots view (smallest theta)
    line_candidates = []
    if FOLLOW_RIGHT:
        line_candidates = right_list
    else:
        line_candidates = left_list
    #print(line_candidates)
    for line in line_candidates:
        angle = np.arctan2(line[0][1], line[1][1])
        print(angle) #TODO angle not correct!
        pass
    
    #TODO translate that line towards the robot, by the distance from the robot
    #TODO follow line
    
    if SHOWLINES is not "none":
        right_list_g = sensorUtilities.transformPolylinesL2G(right_list, myWorld.getTrueRobotPose())
        left_list_g = sensorUtilities.transformPolylinesL2G(left_list, myWorld.getTrueRobotPose())
        lines_g = sensorUtilities.transformPolylinesL2G(lines_l, myWorld.getTrueRobotPose())
        if SHOWLINES is "right":
            myWorld.drawPolylines(right_list_g, "pink")
        elif SHOWLINES is "left":
            myWorld.drawPolylines(left_list_g, "light green")
        elif SHOWLINES is "alternate":
            if alternate:
                myWorld.drawPolylines(right_list_g, "pink")
                alternate = False
            else:
                myWorld.drawPolylines(left_list_g, "light green")
                alternate = True
        elif SHOWLINES is "all":
            myWorld.drawPolylines(lines_g, "white")
        

myWorld.close(False)