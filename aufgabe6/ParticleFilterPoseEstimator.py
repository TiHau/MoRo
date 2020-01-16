import numpy as np
import random

from Robot_Simulator_V3 import Robot, sensorUtilities


class ParticleFilterPoseEstimator:

    def __init__(self):
        self.Particles = []

    def initialize(self, poseTo, poseFrom, n=200):
        x1, y1, theta1 = poseTo
        x2, y2, theta2 = poseFrom
        self.Particles = []
        for _ in range(n):
            x = np.random.uniform(x1, x2)
            y = np.random.uniform(y1, y2)
            theta = np.random.uniform(theta1, theta2)
            pose = [x, y, theta]
            self.Particles.append(pose)

    def integrateMovement(self, motion):
        tmpRobot = Robot.Robot()
        v = motion[0]
        omega = motion[1]

        # translational and rotational speed is limited:
        if omega > tmpRobot._maxOmega:
            omega = tmpRobot._maxOmega
        if omega < -tmpRobot._maxOmega:
            omega = -tmpRobot._maxOmega
        if v > tmpRobot._maxSpeed:
            v = tmpRobot._maxSpeed
        if v < -tmpRobot._maxSpeed:
            v = -tmpRobot._maxSpeed

        newPoses = []
        for pose in self.Particles:
            # Add noise to v:
            sigma_v_2 = (tmpRobot._k_d / tmpRobot._T) * abs(v)
            v_noisy = v + random.gauss(0.0, np.sqrt(sigma_v_2))

            # Add noise to omega:
            sigma_omega_tr_2 = (tmpRobot._k_theta / tmpRobot._T) * abs(omega)  # turning rate noise
            sigma_omega_drift_2 = (tmpRobot._k_drift / tmpRobot._T) * abs(v)  # drift noise
            omega_noisy = omega + random.gauss(0.0, np.sqrt(sigma_omega_tr_2))
            omega_noisy += random.gauss(0.0, np.sqrt(sigma_omega_drift_2))

            # Set SigmaMotion:
            tmpRobot._SigmaMotion[0, 0] = sigma_v_2
            tmpRobot._SigmaMotion[1, 1] = sigma_omega_tr_2 + sigma_omega_drift_2

            # Move robot in the world (with noise):
            d_noisy = v_noisy * tmpRobot._T
            dTheta_noisy = omega_noisy * tmpRobot._T

            x = pose[0] + d_noisy * np.cos(pose[2] + 0.5 * dTheta_noisy)
            y = pose[1] + d_noisy * np.sin(pose[2] + 0.5 * dTheta_noisy)
            theta = pose[2] + dTheta_noisy
            newPoses.append([x, y, theta])

        self.Particles = newPoses

    def integrateMeasurement(self, dist_list, alpha_list, distanceMap):
        obstacles = [[x, y] for x, y in zip(dist_list, alpha_list) if x is not None]

        chance = []
        weightedParticles = []  # Diese Liste enthält die Partikel mehrfach entsprechend ihrem Gewicht
        for i in range(len(self.Particles)):
            pose = self.Particles[i]
            prob = 1.0
            for obstacle in obstacles:
                coord = sensorUtilities.transformPolarCoordL2G([obstacle[0]], [obstacle[1]], pose)
                x, y = coord[0]
                dist = distanceMap.getValue(x, y)
                if dist is not None:
                    p = (1 / (np.sqrt(0.0032 * np.pi))) * np.exp(-0.5 * (dist ** 2) / 0.0032)
                    prob = prob * p
            chance.append(prob)
            weightedParticles.append(i)

        # Gewichtete partikelliste erstellen
        chance = chance / np.sum(chance)
        poseList = []
        ran = np.random.choice(weightedParticles, size=len(self.Particles), p=chance)
        for r in ran:
            poseList.append(self.Particles[r])
        self.Particles = poseList

    def getPose(self):
        return np.mean(self.Particles, axis=0)
