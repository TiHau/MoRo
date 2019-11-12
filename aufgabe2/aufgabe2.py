from aufgabe1.aufgabe1 import *

t_O_R = np.dot(trans((2, 1, 0.1)), rot2trans(rotz(np.radians(30))))

t_R_S0 = trans((0.25, 0, 0.2)).dot(rot2trans(rotz(np.radians(40))))

t_S0_S1 = trans((0, -0.05, 0.05)).dot(rot2trans(np.dot(rotx(np.radians(90)), rotz(np.radians(30)))))

t_S1_S2 = trans((0.5, 0, 0)).dot(rot2trans(rotz(np.radians(-10))))

res = t_O_R.dot(t_R_S0).dot(t_S0_S1).dot(t_S1_S2)

print(res.round(5))

print(np.dot(res, (0.5, 0, 0, 1)).round(5))


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


p_R = (0.99163013, 0.58034659, 0.62101007, 1)
l1 = 0.5
l2 = 0.5

# p in KS von Drehteller verschieben
p_DT = np.dot(np.linalg.inv(trans((0.3, 0, 0.20))), p_R)

alpha = get_alpha(p_DT[0], p_DT[1])

print("Alpha: " + str(np.degrees(alpha)))

# KS um alph rotieren
p_DTx = np.dot(np.linalg.inv(rot2trans(rotz(alpha))), p_DT)

beta2 = get_beta2(p_DTx[0], p_DTx[2], l1, l2)

print("Beta2: " + str(np.degrees(beta2)))

beta1 = get_beta1(p_DTx[0], p_DTx[2], l1, l2, beta2)

print("Beta1: " + str(np.degrees(beta1)))
