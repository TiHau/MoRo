from aufgabe1.aufgabe1 import *

if __name__ == "__main__":
    t_O_R = np.dot(trans((2, 1, 0.1)), rot2trans(rotz(np.radians(30))))

    t_R_S0 = trans((0.25, 0, 0.2)).dot(rot2trans(rotz(np.radians(40))))

    t_S0_S1 = trans((0, -0.05, 0.05)).dot(rot2trans(np.dot(rotx(np.radians(90)), rotz(np.radians(30)))))

    t_S1_S2 = trans((0.5, 0, 0)).dot(rot2trans(rotz(np.radians(-10))))

    res = t_O_R.dot(t_R_S0).dot(t_S0_S1).dot(t_S1_S2)

    print(res.round(5))

    print(np.dot(res, (0.5, 0, 0, 1)).round(5))
