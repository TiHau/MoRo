from Robot_Simulator_V3 import simpleWorld

if __name__ == "__main__":
    myWorld = simpleWorld.buildWorld()
    grid = myWorld.getDistanceGrid()
    grid.drawGrid()
