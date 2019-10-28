import numpy as np
import aufgabe1.aufgabe1 as a1

t_O_S0 = np.dot(a1.trans((2, 1, 0.1)), a1.rot2trans(a1.rotz(np.radians(30)))).round(5)
t_S0_S1 = np.dot(a1.trans((0.15, 0, 0.25)),
                 a1.rot2trans(np.dot(a1.rotz(np.radians(40)), a1.roty(np.radians(30))))).round(5)
t_S1_S2 = np.dot(a1.trans((0.5, 0, 0)), a1.rot2trans(a1.roty(np.radians(-10)))).round(5)

res = t_O_S0.dot(t_S0_S1).dot(t_S1_S2).dot(a1.trans((0.5, 0, 0)))

print(np.dot(res, (0, 0, 0, 1)))
