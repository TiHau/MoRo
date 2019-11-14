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


def test():
    # Aufgabe 2.1 a)
    print("T (A nach B)")
    rZ = rotz(np.radians(180))
    tl = trans((-2, 0, 0))
    rot = rot2trans(rZ)
    t_ab = tl.dot(rot).round()
    print(t_ab)

    print()

    print("T (B nach C)")
    rZ = rotz(np.radians(-90))
    tl = trans((-4, -1, 0))
    rot = rot2trans(rZ)
    t_bc = tl.dot(rot).round()
    print(t_bc)

    print()

    print("T (A nach C)")
    rZ = rotz(np.radians(90))
    tl = trans((2, 1, 0))
    rot = rot2trans(rZ)
    t_ac = tl.dot(rot).round()
    print(t_ac)

    print("Aufgbae 2b   T (A nach C)")
    print(np.array_equal(t_ab.dot(t_bc), t_ac))

    print()

    print("Aufgbae 2c   T (A nach C) invertierung überprüfen")
    rZ = rotz(np.radians(-90))
    tl = trans((-1, 2, 0))
    rot = rot2trans(rZ)
    t_ca = tl.dot(rot).round()
    print(np.array_equal(np.linalg.inv(t_ac), t_ca))

    print()

    print("Aufgabe 2d")
    p_b = (-3, 1, 0, 1)

    p_a = np.dot(t_ab, p_b)
    print(p_a)
