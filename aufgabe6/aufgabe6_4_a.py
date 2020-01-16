import numpy as np

from PoseEstimator import plotUtilities
from Robot_Simulator_V3 import simpleWorld, Robot
from aufgabe6.ParticleFilterPoseEstimator import ParticleFilterPoseEstimator

if __name__ == "__main__":
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