import numpy as np
from scipy.optimize import minimize

# Parameterdefinition für jedes Kraftwerk
# Kraftwerk 1
P1_max = 125
P1_min = -125
change_rate1 = 250
gamma1 = 5  # Kostenfaktor für Änderungsrate

# Kraftwerk 2
P2_max = 125
P2_min = -125
change_rate2 = 25
gamma2 = 3

# Kraftwerk 3
P3_max = 150
P3_min = -150
change_rate3 = 15
gamma3 = 2

# Kraftwerk 4
P4_max = 300
P4_min = -300
change_rate4 = 2
gamma4 = 1

# Leistungsbedarf und Strafkosten
P_required = 122  # Zielleistung nach 15 Minuten
penalty_per_mw_missing = 0.10  # Strafkosten pro MW, das fehlt

# Anzahl der Zeitschritte (15 Minuten)
T = 15

# Kostenfunktion für die Optimierung
def cost_function(P):
    # Umformen des Vektors P in ein 4xT Array für die Leistung der Kraftwerke
    P1 = P[:T]
    P2 = P[T:2*T]
    P3 = P[2*T:3*T]
    P4 = P[3*T:]

    total_cost = 0

    # Berechnung der Kosten über alle Zeitschritte
    for t in range(T):
        # Betriebskosten (je schneller die maximale Änderungsrate, desto höher die Kosten)
        cost1 = gamma1 * abs(P1[t])
        cost2 = gamma2 * abs(P2[t])
        cost3 = gamma3 * abs(P3[t])
        cost4 = gamma4 * abs(P4[t])

        # Änderungskosten (quadratisch oder linear)
        if t > 0:
            change_cost1 = gamma1 * (P1[t] - P1[t-1]) ** 2
            change_cost2 = gamma2 * (P2[t] - P2[t-1]) ** 2
            change_cost3 = gamma3 * (P3[t] - P3[t-1]) ** 2
            change_cost4 = gamma4 * (P4[t] - P4[t-1]) ** 2
        else:
            change_cost1 = change_cost2 = change_cost3 = change_cost4 = 0

        # Strafkosten für Fehlleistung
        total_power = P1[t] + P2[t] + P3[t] + P4[t]
        power_deficit = max(0, P_required - total_power)
        penalty_cost = penalty_per_mw_missing * power_deficit

        # Gesamtkosten für diesen Zeitschritt
        total_cost += cost1 + cost2 + cost3 + cost4 + change_cost1 + change_cost2 + change_cost3 + change_cost4 + penalty_cost

    return total_cost

# Nebenbedingungen
constraints = []

# Leistungs- und Änderungsbeschränkungen pro Minute
for t in range(T):
    # Grenzen für Leistung jedes Kraftwerks
    constraints.append({'type': 'ineq', 'fun': lambda P, t=t: P[t] - P1_min})
    constraints.append({'type': 'ineq', 'fun': lambda P, t=t: P1_max - P[t]})
    constraints.append({'type': 'ineq', 'fun': lambda P, t=t: P[T + t] - P2_min})
    constraints.append({'type': 'ineq', 'fun': lambda P, t=t: P2_max - P[T + t]})
    constraints.append({'type': 'ineq', 'fun': lambda P, t=t: P[2*T + t] - P3_min})
    constraints.append({'type': 'ineq', 'fun': lambda P, t=t: P3_max - P[2*T + t]})
    constraints.append({'type': 'ineq', 'fun': lambda P, t=t: P[3*T + t] - P4_min})
    constraints.append({'type': 'ineq', 'fun': lambda P, t=t: P4_max - P[3*T + t]})
    
    # Beschränkungen für Änderungsrate (außer im ersten Zeitschritt)
    if t > 0:
        constraints.append({'type': 'ineq', 'fun': lambda P, t=t: change_rate1 - abs(P[t] - P[t-1])})
        constraints.append({'type': 'ineq', 'fun': lambda P, t=t: change_rate2 - abs(P[T + t] - P[T + t - 1])})
        constraints.append({'type': 'ineq', 'fun': lambda P, t=t: change_rate3 - abs(P[2*T + t] - P[2*T + t - 1])})
        constraints.append({'type': 'ineq', 'fun': lambda P, t=t: change_rate4 - abs(P[3*T + t] - P[3*T + t - 1])})

# Bedingung für den Leistungsbedarf in der letzten Minute
constraints.append({'type': 'eq', 'fun': lambda P: P[T-1] + P[2*T-1] + P[3*T-1] + P[4*T-1] - P_required})

# Startwerte für die Optimierung (zunächst gleiche Verteilung)
initial_guess = np.full(4 * T, P_required / 4)

# Optimierung durchführen
result = minimize(cost_function, initial_guess, constraints=constraints)

# Ergebnis anzeigen
if result.success:
    P_opt = result.x
    P1_opt = P_opt[:T]
    P2_opt = P_opt[T:2*T]
    P3_opt = P_opt[2*T:3*T]
    P4_opt = P_opt[3*T:]
    
    print("Optimierte Leistung pro Minute:")
    for t in range(T):
        print(f"Minute {t+1}: Kraftwerk 1 = {P1_opt[t]:.2f} MW, Kraftwerk 2 = {P2_opt[t]:.2f} MW, Kraftwerk 3 = {P3_opt[t]:.2f} MW, Kraftwerk 4 = {P4_opt[t]:.2f} MW")
    print(f"Minimale Gesamtkosten über 15 Minuten: {result.fun:.2f} Euro")
else:
    print("Optimierung fehlgeschlagen:", result.message)
