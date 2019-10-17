import numpy as np


def rot(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array(((c, -s),
                     (s, c)))


def rotx(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array(((1, 0, 0),
                     (0, c, -s),
                     (0, s, c)))


def roty(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array(((c, 0, s),
                     (0, 1, 0),
                     (-s, 0, c)))


def rotz(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array(((c, -s, 0),
                     (s, c, 0),
                     (0, 0, 1)))


def rot2trans(r):
    if len(r) is 2:  # len(np.array) liefert die Dimension zurück
        return np.array(((r[0, 0], r[0, 1], 0),
                         (r[1, 0], r[1, 1], 0),
                         (0, 0, 1)))
    return np.array(((r[0, 0], r[0, 1], r[0, 2], 0),
                     (r[1, 0], r[1, 1], r[1, 2], 0),
                     (r[2, 0], r[2, 1], r[2, 2], 0),
                     (0, 0, 0, 1)))


def trans(t):
    if len(t) is 2:
        return np.array(((1, 0, t[0]),
                         (0, 1, t[1]),
                         (0, 0, 1)))
    return np.array(((1, 0, 0, t[0]),
                     (0, 1, 0, t[1]),
                     (0, 0, 1, t[2]),
                     (0, 0, 0, 1)))


# Aufgabe 2.1 a)
print("T (A nach B)")
rZ = rotz(np.radians(180))
tl = trans((-2, 0, 0))
rot = rot2trans(rZ)
t = tl.dot(rot)
print(t.round())

print()

print("T (B nach C)")
rZ = rotz(np.radians(-90))
tl = trans((-4, -1, 0))
rot = rot2trans(rZ)
t = tl.dot(rot)
print(t.round())

print()

print("T (A nach C)")
rZ = rotz(np.radians(90))
tl = trans((2, 1, 0))
rot = rot2trans(rZ)
t = tl.dot(rot)
print(t.round())
