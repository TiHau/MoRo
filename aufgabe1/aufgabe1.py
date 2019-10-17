import numpy as np

def rot(theta):
	c, s = np.cos(theta), np.sin(theta)
	return np.array(((c, -s), 
					 (s,  c)))

def rotx(theta):
	c, s = np.cos(theta), np.sin(theta)
	return np.array(((1,  0,  0), 
					 (0,  c, -s),
					 (0,  s,  c)))

def roty(theta):
	c, s = np.cos(theta), np.sin(theta)
	return np.array(((c,  0,  s), 
					 (0,  1,  0), 
					 (-s, 0,  c)))

def rotz(theta):
	c, s = np.cos(theta), np.sin(theta)
	return np.array(((c, -s,  0), 
					 (s,  c,  0),
					 (0,  0,  1)))

def rot2trans(r):
	pass

def trans(t):
	pass