import numpy as np

# Eigenschaften der Kraftwerke
max_leistungen = np.array([300, 150, 125, 125], dtype=float)  # maximale Leistungen in MW
steigerraten = np.array([2, 15, 25, 125], dtype=float)  # Erhöhungen pro Zeitschritt in MW

# Ziel-Regelleistung
ziel_regelleistung = 467

# Speichere die Ergebnisse
results = []

# Anzahl der Zeitschritte
zeitschritte = 0

# Solange die Ziel-Regelleistung nicht erreicht ist
while True:
    zeitschritte += 1
    
    # Berechnung der maximalen Erhöhung für diesen Zeitschritt
    aktuelle_max_leistungen = steigerraten * zeitschritte
    
    # Gesamtmaximale Leistung, die in diesem Zeitschritt erreichbar ist
    max_gesamt_leistung = np.sum(np.minimum(aktuelle_max_leistungen, max_leistungen))

    if max_gesamt_leistung < ziel_regelleistung:
        # Wenn die maximale erreichbare Leistung kleiner ist als das Ziel,
        # setze alle Kraftwerke auf ihre maximalen Leistungen
        aktuelle_leistungen = np.minimum(max_leistungen, aktuelle_max_leistungen)
    else:
        # Initialisiere die aktuellen Leistungen mit den maximalen Erhöhungen
        aktuelle_leistungen = np.minimum(aktuelle_max_leistungen, max_leistungen)

        # Berechnung der aktuellen Gesamtleistung
        gesamtleistung = np.sum(aktuelle_leistungen)

        # Wenn die Gesamtleistung die Ziel-Regelleistung übersteigt,
        # müssen wir die Verteilung so anpassen, dass die Summe 500 MW ergibt
        if gesamtleistung > ziel_regelleistung:
            # Berechne den Anpassungsfaktor
            faktor = ziel_regelleistung / gesamtleistung
            aktuelle_leistungen *= faktor  # jetzt aktuelle_leistungen ist float

            # Runde die Ergebnisse auf, um sie als Ganzzahlen darzustellen
            aktuelle_leistungen = np.round(aktuelle_leistungen)

            # Falls die Rundung zu einer Über- oder Unterschreitung führt,
            # passen wir die Werte so an, dass sie die Maximalgrenzen nicht überschreiten
            while np.sum(aktuelle_leistungen) != ziel_regelleistung:
                # Finden Sie das Kraftwerk mit dem größten Erhöhungspotential
                for i in range(len(aktuelle_leistungen)):
                    if aktuelle_leistungen[i] < max_leistungen[i]:
                        aktuelle_leistungen[i] += 1
                        if np.sum(aktuelle_leistungen) == ziel_regelleistung:
                            break
                    if np.sum(aktuelle_leistungen) > ziel_regelleistung:
                        aktuelle_leistungen[i] -= 1
                        break

    # Ergebnisse speichern
    results.append(aktuelle_leistungen)

    # Prüfen, ob die Ziel-Regelleistung erreicht wurde
    if np.sum(aktuelle_leistungen) >= ziel_regelleistung:
        break

    print(f"Zeitschritt: {zeitschritte}")
    print(f"Bereitgestellte Leistungen: {aktuelle_leistungen}")
    print(f"Aktuelle Gesamtleistung: {np.sum(aktuelle_leistungen)}\n")

# Ergebnisse ausgeben
results = np.array(results)
print("Steuerparameter-Matrix (Kraftwerke A, B, C, D in den Zeitschritten):")
print(results)
print(f"Anzahl der benötigten Zeitschritte: {zeitschritte}")
