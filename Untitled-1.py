import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# CSV-Datei einlesen
df = pd.read_csv("data/Leistungskurve Nordex N29.csv", delimiter=";")

# Funktion definieren
def power_function(x, a, b, c, d):
    y = np.zeros_like(x)
    y = np.where(x < 3, 0, y)
    y = np.where((x >= 3) & (x <= 15), a * np.power(x, 3) + b * np.power(x, 2) + c * x + d, y)
    y = np.where((x > 15) & (x <= 25), 250, y)
    y = np.where(x > 25, 0, y)
    return y

# Fit durchführen
x_data = df["Windgeschwindigkeit (ms)"]
y_data = df["Leistung (kW)"]

# Randbedingungen
a_init = (0 - 250) / np.power(3, 3)
b_init = 0
c_init = (250 - 0) / 15
d_init = 0

popt, _ = curve_fit(power_function, x_data, y_data, p0=[a_init, b_init, c_init, d_init])

# Funktion mit Fit-Parametern erstellen
def fitted_function(x):
    return power_function(x, *popt)

# Plot erstellen
x_range = np.linspace(0, 30, 100)  # Range für x-Werte
plt.figure(figsize=(8, 6))
plt.scatter(x_data, y_data, label="Originaldaten")
plt.plot(x_range, fitted_function(x_range), 'r-', label="Fit-Funktion")
plt.xlabel("Windgeschwindigkeit (ms)")
plt.ylabel("Leistung (kW)")
plt.title("Leistungskurve")
plt.legend()
plt.grid(True)
plt.show()
