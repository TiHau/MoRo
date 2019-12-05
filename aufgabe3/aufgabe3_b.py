import numpy as np
from Robot_Simulator_V3 import World, Robot
import Robot_Simulator_V3.geometry as geo


# Länge(Betrag) eines 2D-Vektors
def vectorLength(v):
    return (np.sqrt(v[0] ** 2 + v[1] ** 2))[0]


def followLine(robot, world, p_x, p_y):
    p_x_x, p_x_y = p_x
    p_y_x, p_y_y = p_y

    g = np.array([p_y_x - p_x_x, p_y_y - p_x_y])

    x, y, theta = world.getTrueRobotPose()

    e = geo.normalToLine((x, y), (p_x, p_y))

    r = g / np.linalg.norm(g)

    er = np.add(e, r)

    xv = [er[0], 0]

    print(er)
    print(xv)


def gotoGlobal(robot, world, v, p, tol):
    p_x, p_y = p

    # Robotposition bestimmen:
    (x, y, theta) = world.getTrueRobotPose()

    while True:
        distance = vectorLength(np.array([[p_x - x], [p_y - y]]))
        if distance < tol:  # Punkt erreicht
            break

        (x, y, theta) = world.getTrueRobotPose()
        theta = np.degrees(theta)
        thetaStern = np.degrees(np.arctan2(p_y - y, p_x - x))
        diff = (thetaStern - theta) % 360

        if diff > 180:
            diff = diff - 360

        omega = np.radians(diff)

        if abs(diff) > 5:
            robot.move([0, omega])
        else:
            robot.move([v, omega])
    return


def followPolyline(robot, world, v, polyline):
    for p in polyline:
        gotoGlobal(robot, world, v, p, 0.1)
    return


myWorld = World.World(20, 10)

myWorld.addLine(1, 5, 10, 5)
myWorld.addLine(11, 5, 19, 5)
myWorld.addLine(1, 7, 19, 7)
myWorld.addLine(11, 5, 11, 3.5)
myWorld.addLine(11, 2.5, 11, 1)

polyline = [[1, 6], [10.5, 6], [10.5, 3], [15, 3]]
myWorld.drawPolyline(polyline)

myRobot = Robot.Robot()
myWorld.setRobot(myRobot, [1, 6, 0])

followPolyline(myRobot, myWorld, 1, polyline)
