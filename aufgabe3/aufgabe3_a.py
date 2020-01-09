from Robot_Simulator_V3 import emptyWorld
from Robot_Simulator_V3 import Robot
from numpy import pi, radians


def curveDrive(robot, v, r, delta_theta):
    turn_right = delta_theta < 0
    delta_theta = radians(delta_theta)
    omega = v / r
    if turn_right:
        omega = -omega
    time_needed = delta_theta / omega
    n = int(time_needed / robot.getTimeStep())
    for t in range(n):
        robot.move((v, omega))


def straightDrive(robot, v, l):
    n = int((l / v) / robot.getTimeStep())

    for t in range(n):
        robot.move((v, 0))


# myWorld = emptyWorld.buildWorld()
# myRobot = Robot.Robot()
# myWorld.setRobot(myRobot, [3, 3, pi / 2])
#
# straightDrive(myRobot, 1, 5)
# curveDrive(myRobot, 1, 4, -180)
# straightDrive(myRobot, 1, 5)
#
# myWorld.close()
