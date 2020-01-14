import numpy as np
from Robot_Simulator_V3 import simpleWorld
from Robot_Simulator_V3 import Robot


def curveDrive(robot, world, v=1, r=4, deltaTheta=-np.pi, n=100):
    omega = v / r * np.sign(deltaTheta)
    robot.setTimeStep(abs(deltaTheta / omega))

    poses = [world.getTrueRobotPose()]

    for _ in range(n):
        robot.move([v / n, omega / n])
        poses.append(world.getTrueRobotPose())
    return poses


if __name__ == "__main__":
    myWorld = simpleWorld.buildWorld()
    myRobot = Robot.Robot()
    myWorld.setRobot(myRobot, [4, 4, np.pi / 2])
    print(curveDrive(myRobot, myWorld))
    myWorld.close()
