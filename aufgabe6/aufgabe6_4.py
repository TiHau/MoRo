import numpy as np
import matplotlib.pyplot as plt

from PoseEstimator import plotUtilities
from Robot_Simulator_V3 import simpleWorld, Robot
from aufgabe6.ParticleFilterPoseEstimator import ParticleFilterPoseEstimator


def test_teil_a():
    myWorld = simpleWorld.buildWorld()
    myRobot = Robot.Robot()
    myWorld.setRobot(myRobot, [4, 4, np.pi / 2])

    myParticle = ParticleFilterPoseEstimator()
    myParticle.initialize([3, 3, np.pi / 3], [5, 5, (np.pi / 3) * 2], 200)

    plotUtilities.plotPoseParticles(myParticle.Particles, color='g')

    for _ in range(500):
        myParticle.integrateMovement([1, np.pi / 2])

    plotUtilities.plotPoseParticles(myParticle.Particles, color='r')

    plotUtilities.plotShow()

    myWorld.close()


def test_teil_b():
    myWorld = simpleWorld.buildWorld()
    myRobot = Robot.Robot()
    myWorld.setRobot(myRobot, [4, 4, np.pi / 2])
    myParticle = ParticleFilterPoseEstimator()

    myParticle.initialize([3, 3, np.pi / 3], [5, 5, (np.pi / 3) * 2], 200)

    print('True Position: ', str(myWorld.getTrueRobotPose()))
    print('Random Particles: ', str(myParticle.getPose()))

    plotUtilities.plotPoseParticles(myParticle.Particles, color='g')

    myParticle.integrateMeasurement(myRobot.sense(), myRobot.getSensorDirections(), myWorld.getDistanceGrid())
    plotUtilities.plotPoseParticles(myParticle.Particles, color='r')

    print('Weighted Particles: ', str(myParticle.getPose()))
    plt.plot([2, 16, 16, 4, 4, 2, 2], [2, 2, 12, 12, 10, 10, 2], 'k-')
    plotUtilities.plotShow()

    myWorld.close()


def test_teil_c():
    myWorld = simpleWorld.buildWorld()
    myRobot = Robot.Robot()
    myWorld.setRobot(myRobot, [4, 4, np.pi / 2])
    myParticle = ParticleFilterPoseEstimator()
    myParticle.initialize([3, 3, np.pi / 3], [5, 5, (np.pi / 3) * 2], 500)
    plotUtilities.plotPoseParticles(myParticle.Particles, color='r')

    v = 1
    r = 4
    deltaTheta = -np.pi
    n = 100

    omega = v / r * np.sign(deltaTheta)
    myRobot.setTimeStep(abs(deltaTheta / omega))

    realPoses = [myWorld.getTrueRobotPose()]
    filterPoses = [myParticle.getPose()]

    for _ in range(n):
        myRobot.move([v / n, omega / n])
        realPoses.append(myWorld.getTrueRobotPose())

        myParticle.integrateMovement([v, omega])
        myParticle.integrateMeasurement(myRobot.sense(), myRobot.getSensorDirections(), myWorld.getDistanceGrid())
        filterPoses.append(myParticle.getPose())

    plotUtilities.plotPositions(realPoses, 'b')
    plotUtilities.plotPositions(filterPoses, 'g')

    plotUtilities.plotPoseParticles(myParticle.Particles, color='r')

    plt.plot([2, 16, 16, 4, 4, 2, 2], [2, 2, 12, 12, 10, 10, 2], 'k-')
    plotUtilities.plotShow()
    myWorld.close()


def test_teil_d():
    myWorld = simpleWorld.buildWorld()
    myWorld.addLine(2, 6, 4, 6)
    myWorld.addLine(6, 2, 6, 6)
    myWorld.addLine(6, 6, 10, 6)
    myWorld.addLine(4, 10, 16, 10)
    myRobot = Robot.Robot()
    myWorld.setRobot(myRobot, [4, 4, np.pi / 2])
    myParticle = ParticleFilterPoseEstimator()
    myParticle.initialize([3, 3, np.pi / 3], [5, 5, (np.pi / 3) * 2], 500)
    plotUtilities.plotPoseParticles(myParticle.Particles, color='r')

    v = 1
    r = 4
    deltaTheta = -np.pi
    n = 100

    omega = v / r * np.sign(deltaTheta)
    myRobot.setTimeStep(abs(deltaTheta / omega))

    realPoses = [myWorld.getTrueRobotPose()]
    filterPoses = [myParticle.getPose()]

    for i in range(n):
        myRobot.move([v / n, omega / n])
        realPoses.append(myWorld.getTrueRobotPose())
        myParticle.integrateMovement([v, omega])
        myParticle.integrateMeasurement(myRobot.sense(), myRobot.getSensorDirections(), myWorld.getDistanceGrid())
        filterPoses.append(myParticle.getPose())

        if i % (n / 10) == 0:
            plotUtilities.plotPositions(realPoses, 'b')
            plotUtilities.plotPositions(filterPoses, 'g')
            plotUtilities.plotPoseParticles(myParticle.Particles, color='r')
            plt.plot([2, 16, 16, 4, 4, 2, 2], [2, 2, 12, 12, 10, 10, 2], 'k-')
            plotUtilities.plotShow()
            plt.close()

    myWorld.close()


if __name__ == "__main__":
    test_teil_d()
