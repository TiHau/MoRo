import numpy as np
import matplotlib.pyplot as plt

from PoseEstimator import plotUtilities
from Robot_Simulator_V3 import simpleWorld, Robot
from aufgabe6.ParticleFilterPoseEstimator import ParticleFilterPoseEstimator

if __name__ == "__main__":
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
