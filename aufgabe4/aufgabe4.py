from Robot_Simulator_V3 import labyrinthWorld
from Robot_Simulator_V3 import Robot
from Robot_Simulator_V3 import sensorUtilities
import Robot_Simulator_V3.geometry as geo
import numpy as np

myWorld = labyrinthWorld.buildWorld()
myRobot = Robot.Robot()
myWorld.setRobot(myRobot, [3, 18, 0])

OMEGA_DEF = 0.3

def vectorLength(v):
    return (np.sqrt(v[0] ** 2 + v[1] ** 2))

def followLine(p1, p2, tol=0.1, v=0.5):
    p1_x, p1_y = p1
    p2_x, p2_y = p2
    
    g = np.array([p2_x - p1_x, p2_y - p1_y])
    distance = vectorLength(np.array([[p2_x], [p2_y]]))
    if distance < tol:  # Punkt erreicht
        myRobot.move([v/2, -OMEGA_DEF])
        return
    x, y = 0, 0
    e = geo.normalToLine((x, y), (p1, p2))
    r = g / np.linalg.norm(g)
    er = np.add(e, r)
    goto_x, goto_y = np.add([x, y], er)
    thetaStern = np.degrees(np.arctan2(goto_y, goto_x))
    diff = (thetaStern) % 360
    if diff > 180:
        diff = diff - 360
    omega = np.radians(diff)
    myRobot.move([v, omega])

def wander(limit = 1, v = 0.3, o = 0.5):
    sensor_l = myRobot.sense()[16]
    sensor_m = myRobot.sense()[13]
    sensor_r = myRobot.sense()[10]
    if sensor_m and sensor_m < limit:
        myRobot.move([-v, o])
    elif sensor_l and sensor_l < limit:
        myRobot.move([0, -o])
    elif sensor_r and sensor_r < limit:
        myRobot.move([0, o])
    else:
        myRobot.move([v, 0])
    return

def followWall(v = 0.5, d = 0.75, offset = 1):
    directions = myRobot.getSensorDirections()[2:10]
    middle_sensor = myRobot.sense()[13]
    sensors = myRobot.sense()[3:9]
    for i, sensor in enumerate(sensors):
        if sensor != None and sensor > d + 0.3:
            sensors[i] = None
    wall_candidates = sensorUtilities.extractSegmentsFromSensorData(sensors, directions)
    if len(wall_candidates) > 0:
        start = wall_candidates[0][0]
        start[1] = start[1] + offset
        end = wall_candidates[0][1]
        end[1] = end[1] + offset
        wall = [[start, end]]
        lines = sensorUtilities.transformPolylinesL2G(wall, myWorld.getTrueRobotPose())
        myWorld.drawPolylines(lines)
        if middle_sensor != None and middle_sensor < d:
            myRobot.move([0, OMEGA_DEF])
        else:
            followLine(start, end)
    else:
        myRobot.move([v/2, -OMEGA_DEF])

while True:
    #wander()
    followWall()
myWorld.close(False)