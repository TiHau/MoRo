import numpy as np
from Robot_Simulator_V3 import World, Robot
import Robot_Simulator_V3.geometry as geo


# Länge(Betrag) eines 2D-Vektors
def vectorLength(v):
    return (np.sqrt(v[0] ** 2 + v[1] ** 2))  # [0]


def followLine(robot, world, p1, p2, tol=0.1, v=0.5):
    p1_x, p1_y = p1
    p2_x, p2_y = p2

    while True:
        g = np.array([p2_x - p1_x, p2_y - p1_y])

        x, y, theta = world.getTrueRobotPose()

        distance = vectorLength(np.array([[p2_x - x], [p2_y - y]]))
        if distance < tol:  # Punkt erreicht
            break

        e = geo.normalToLine((x, y), (p1, p2))

        r = g / np.linalg.norm(g)

        er = np.add(e, r)

        goto_x, goto_y = np.add([x, y], er)

        theta = np.degrees(theta)
        thetaStern = np.degrees(np.arctan2(goto_y - y, goto_x - x))
        diff = (thetaStern - theta) % 360

        if diff > 180:
            diff = diff - 360

        omega = np.radians(diff)

        robot.move([v, omega])


def gotoGlobal(robot, world, v, p, tol):
    p_x, p_y = p

    while True:
        (x, y, theta) = world.getTrueRobotPose()

        distance = vectorLength(np.array([[p_x - x], [p_y - y]]))
        if distance < tol:  # Punkt erreicht
            break

        theta = np.degrees(theta)
        thetaStern = np.degrees(np.arctan2(p_y - y, p_x - x))
        diff = (thetaStern - theta) % 360

        if diff > 180:
            diff = diff - 360

        omega = np.radians(diff)

        # Setzt v auf 0, wenn der Roboter sich neu ausrichten soll. Sorgt für genaues abfahren der Linie
        if abs(diff) > 5:
            robot.move([0, omega])
        else:
            robot.move([v, omega])
    return


def followPolyline_MitGoToGlobal(robot, world, v, polyline, tol):
    for p in polyline:
        gotoGlobal(robot, world, v, p, tol)
    return


def followPolyline_MitFollowLine(robot, world, v, polyline, tol):
    for i in range(len(polyline) - 1):
        followLine(robot, world, polyline[i], polyline[i + 1], tol, v)


def test_followLine():
    myWorld = World.World(20, 10)

    myWorld.drawPolyline([[1, 4], [15, 4]])

    myRobot = Robot.Robot()
    myWorld.setRobot(myRobot, [3, 6, np.radians(90)])

    followLine(myRobot, myWorld, [1, 4], [15, 4])


def test_followPoly_GotoGlobal():
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

    followPolyline_MitGoToGlobal(myRobot, myWorld, 1, polyline, 0.1)


def test_followPoly_FollowLine():
    myWorld = World.World(20, 10)

    myWorld.addLine(1, 5, 10, 5)
    myWorld.addLine(11, 5, 19, 5)
    myWorld.addLine(1, 7, 19, 7)
    myWorld.addLine(11, 5, 11, 3.5)
    myWorld.addLine(11, 2.5, 11, 1)

    polyline = [[1, 6], [10.5, 6], [10.5, 3], [18, 3]]
    myWorld.drawPolyline(polyline)

    myRobot = Robot.Robot()
    myWorld.setRobot(myRobot, [1, 6, 0])

    followPolyline_MitFollowLine(myRobot, myWorld, 0.5, polyline, 0.8)


#test_followLine()
#test_followPoly_GotoGlobal()
#test_followPoly_FollowLine()