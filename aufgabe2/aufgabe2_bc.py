from aufgabe1.aufgabe1 import *
import matplotlib.pyplot as plt


def get_alpha(x_p, y_p):
    return np.arctan(y_p / x_p)


def get_beta2(x_p, y_p, l1, l2):
    top = (x_p * x_p) + (y_p * y_p) - (l1 * l1) - (l2 * l2)
    bottom = 2 * l1 * l2
    return -np.arccos(top / bottom)


def get_beta1(x_p, y_p, l1, l2, beta2):
    first = np.arctan(y_p / x_p)
    top = l2 * np.sin(beta2)
    bottom = l1 + (l2 * np.cos(beta2))
    second = np.arctan(top / bottom)
    return first - second


def invKin(p_R):
    l1 = 0.5
    l2 = 0.5

    # p in KS von Drehteller verschieben
    p_DT = np.dot(np.linalg.inv(trans((0.3, 0, 0.20))), p_R)

    alpha = get_alpha(p_DT[0], p_DT[1])

    # KS um alph rotieren
    p_DTx = np.dot(np.linalg.inv(rot2trans(rotz(alpha))), p_DT)

    beta2 = get_beta2(p_DTx[0], p_DTx[2], l1, l2)

    beta1 = get_beta1(p_DTx[0], p_DTx[2], l1, l2, beta2)

    return alpha, beta1, beta2


def vorKin(p):
    t_R_S0 = trans((0.3, 0, 0.2)).dot(rot2trans(rotz(np.radians(40))))

    t_S0_S1 = rot2trans(np.dot(rotx(np.radians(90)), rotz(np.radians(30))))

    t_S1_S2 = trans((0.5, 0, 0)).dot(rot2trans(rotz(np.radians(-10))))

    t_S2_S3 = trans((0.5, 0, 0, 1))

    res = t_R_S0.dot(t_S0_S1).dot(t_S1_S2).dot(t_S2_S3)

    return res.dot(p)


if __name__ == "__main__":
    test_p = vorKin((0, 0, 0, 1))
    print("Testpunkt: " + str(test_p))

    a, b1, b2 = invKin(test_p)

    print("Alpha, Beta1, Beta2: " + str(np.degrees(a)) + "," + str(np.degrees(b1)) + "," + str(np.degrees(b2)))

    x = 0.8
    r = 0.3
    alphas = []
    beta1s = []
    beta2s = []

    for t in range(0, 360):
        a_tmp, b1_tmp, b2_tmp = invKin((x, r * np.cos(np.radians(t)), r * np.sin(np.radians(t)), 1))
        alphas.append(np.degrees(a_tmp))
        beta1s.append(np.degrees(b1_tmp))
        beta2s.append(np.degrees(b2_tmp))

    plt.plot(alphas)
    plt.plot(beta1s)
    plt.plot(beta2s)
    plt.legend(["Alpha", "Beta1", "Beta2"])
    plt.show()
