from Robot_Simulator_V3 import twoRoomsWorld
from Robot_Simulator_V3 import Robot
from aufgabe3.aufgabe3_b import gotoGlobal
from aufgabe3.aufgabe3_a import straightDrive
import numpy as np


def turn(robot, delta_theta):
    turn_right = delta_theta < 0
    omega = 0.5
    if not turn_right:
        omega = -omega
    time_needed = abs(delta_theta / omega)
    n = int(time_needed / robot.getTimeStep())
    for t in range(n):
        robot.move((0, omega))


def checkForBox(robot):
    x = np.pi * 2
    omega = 0.3
    time_needed = abs(x / omega)
    n = int(time_needed / robot.getTimeStep())
    while True:
        n = n - 1
        robot.move([0, omega])
        if robot.senseBoxes():
            return robot.senseBoxes()[0]
        if n < 0:
            return None


myWorld = twoRoomsWorld.buildWorld()
myKeyboardController = myWorld.getKeyboardController()
myRobot = Robot.Robot()
myWorld.setRobot(myRobot, [16, 12, 0])

door1_1 = (7, 2.75)
door1_2 = (9, 2.75)
door2_1 = (14, 9.75)
door2_2 = (16, 9.75)

p1 = (4, 11)
p2 = (4, 4)
p3 = (12, 4)
p4 = (12, 11)

depot = (16, 12)

myCheckpoints = [p1, p2, p3, p4]
myWaypoints = [p1, p2, door1_1, door1_2, p3, p4, door2_1, door2_2, depot]

currentCheckpoint = myCheckpoints.pop(0)
tempCheckpoint = None
skip_return = False


def returnFromDepot(checkpoint):
    myWaypoints_rev = reversed(myWaypoints)
    for wp in myWaypoints_rev:
        gotoGlobal(myRobot, myWorld, 1, wp, 0.2)
        if wp is checkpoint:
            return


def gotoDepot(checkpoint):
    found_start = False

    for wp in myWaypoints:
        if found_start:
            gotoGlobal(myRobot, myWorld, 1, wp, 0.2)
            continue

        if wp is checkpoint:
            gotoGlobal(myRobot, myWorld, 1, wp, 0.2)
            found_start = True


def gotoNextCheckpoint(checkpoint, current):
    found_start = False
    for wp in myWaypoints:
        if wp is checkpoint:
            gotoGlobal(myRobot, myWorld, 1, wp, 0.2)
            return
        if wp is current:
            found_start = True
            gotoGlobal(myRobot, myWorld, 1, wp, 0.2)
        if found_start:
            gotoGlobal(myRobot, myWorld, 1, wp, 0.2)


while True:
    # Gehe zum nächsten Checkpoint
    if not skip_return:
        returnFromDepot(currentCheckpoint)
    else:
        last_checkpoint = currentCheckpoint
        currentCheckpoint = myCheckpoints.pop(0)
        gotoNextCheckpoint(currentCheckpoint, last_checkpoint)

    skip_return = False

    # Überprüfe auf Boxen
    boxToPickup = checkForBox(myRobot, myWorld)
    if not boxToPickup:
        if len(myCheckpoints) <= 0:
            # fertig
            break

        skip_return = True

    # Fahre zur gefundenen Box und heb sie auf
    else:
        while boxToPickup:
            turn(myRobot, boxToPickup[1])
            straightDrive(myRobot, 0.5, boxToPickup[0] - 0.2)
            if myRobot.pickUpBox():
                boxToPickup = None
                gotoDepot(currentCheckpoint)
                myRobot.placeBox()
            else: #box wurde nicht aufgehoben
                gotoGlobal(myRobot, myWorld, 0.5, currentCheckpoint, 0.2)
                boxToPickup = checkForBox(myRobot)
