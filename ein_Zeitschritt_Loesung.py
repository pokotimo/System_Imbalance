import numpy as np

# Assets, Maximalleistung 
a = 300
b = 150
c = 125
d = 125

# Steuerungvektoren
alpha = np.arange(-1, 1 + 1/150, 1/150)
beta = np.arange(-1, 1.1, 0.1)
gamma = np.arange(-1, 1.2, 0.2)
delta = np.arange(-1, 2, 1)

# Initialisierung der Steuerparameter
status_a = alpha[150]
status_b = beta[10]
status_c = gamma[5]
status_d = delta[1]

# Ziel-Regelleistung
ziel_regelleistung = 143

# Funktion zur Berechnung der Regelleistung
def berechne_regelleistung(status_a, status_b, status_c, status_d):
    return a * status_a + b * status_b + c * status_c + d * status_d

# Schleife zur Anpassung der Steuerparameter
beste_regelleistung = berechne_regelleistung(status_a, status_b, status_c, status_d)
bester_status = (status_a, status_b, status_c, status_d)

# Wir durchlaufen alle möglichen Kombinationen, die um 1 von den aktuellen Werten abweichen
for da in [-1, 0, 1]:
    for db in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            for dd in [-1, 0, 1]:
                neuer_status_a = alpha[np.clip(150 + da, 0, len(alpha) - 1)]
                neuer_status_b = beta[np.clip(10 + db, 0, len(beta) - 1)]
                neuer_status_c = gamma[np.clip(5 + dc, 0, len(gamma) - 1)]
                neuer_status_d = delta[np.clip(1 + dd, 0, len(delta) - 1)]
                
                regelleistung = berechne_regelleistung(neuer_status_a, neuer_status_b, neuer_status_c, neuer_status_d)

                # Prüfen, ob die neue Regelleistung näher am Ziel ist
                if abs(regelleistung - ziel_regelleistung) < abs(beste_regelleistung - ziel_regelleistung):
                    beste_regelleistung = regelleistung
                    bester_status = (neuer_status_a, neuer_status_b, neuer_status_c, neuer_status_d)

# Ausgabe der besten Steuerparameter und der erreichten Regelleistung
print("Beste Steuerparameter:")
print(f"Status a: {bester_status[0]}")
print(f"Status b: {bester_status[1]}")
print(f"Status c: {bester_status[2]}")
print(f"Status d: {bester_status[3]}")
print(f"Erreichte Regelleistung: {beste_regelleistung}")

