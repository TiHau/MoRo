import numpy as np
import matplotlib.pyplot as plt

from PoseEstimator import plotUtilities
from Robot_Simulator_V3 import simpleWorld, Robot
from aufgabe6.ParticleFilterPoseEstimator import ParticleFilterPoseEstimator

if __name__ == "__main__":
    myWorld = simpleWorld.buildWorld()
    myWorld.addLine(2, 6, 4, 6)
    myWorld.addLine(6, 2, 6, 6)
    myWorld.addLine(6, 6, 10, 6)
    myWorld.addDynObstacleLine(4, 10, 16, 10)
    myRobot = Robot.Robot()
    myWorld.setRobot(myRobot, [4, 4, np.pi / 2])
    myParticle = ParticleFilterPoseEstimator()
    myParticle.initialize([3, 3, np.pi / 3], [5, 5, (np.pi / 3) * 2], 200)
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

        if i in [0, 1, int(n / 2), n - 1]:
            plotUtilities.plotPositions(realPoses, 'b')
            plotUtilities.plotPositions(filterPoses, 'g')
            plotUtilities.plotPoseParticles(myParticle.Particles, color='r')
            plt.plot([2, 16, 16, 4, 4, 2, 2], [2, 2, 12, 12, 10, 10, 2], 'k-')
            plotUtilities.plotShow()
            plt.close()

    myWorld.close()
