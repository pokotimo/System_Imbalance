# Assets, Maximalleistung

a = 300
b = 150
c = 125
d = 125


# Steuerungsfaktoren
import numpy as np

alpha = np.arange(-1, 1 + 1/150, 1/150)
beta = np.arange(-1, 1.1, 0.1)
gamma = np.arange(-1, 1.2, 0.2)
delta = np.arange(-1, 2, 1)

RL = a*alpha + b*beta + c*gamma + d*delta
