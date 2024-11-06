# Assets, Maximalleistung

a = 300
b = 150
c = 125
d = 125


# Steuerungvektoren, von -1 bis 1 in unterschiedlich großen Schritten, 
# entspricht diskreten Lesitungszuständen, die von Kraftwerken eingenommen werden können

import numpy as np

alpha = np.arange(-1, 1 + 1/150, 1/150)
beta = np.arange(-1, 1.1, 0.1)
gamma = np.arange(-1, 1.2, 0.2)
delta = np.arange(-1, 2, 1)


# Initialisierung der Steuerparameter, alle Status von a bis d sind zu beginn auf den 0-Wert gesetzt

status_a = alpha[150]
status_b = beta[10]
status_c = gamma[5]
status_d = delta[1]

# Regelleistung die von a, b, c, d insgesamt ausgeht berechnet sich durch:

RL = a*status_a + b*status_b + c*status_c + d*status_d

SI = [500, 500, 500, 500]


print(alpha[150])
print(beta[10])
print(gamma[5])
print(delta[1])