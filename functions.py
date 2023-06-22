import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

def adjust_wind_speed(wind_speed, hub_height, roughness_length):
    adjusted_speed = wind_speed * (np.log(hub_height / roughness_length) / np.log(10 / roughness_length))
    return adjusted_speed

def fit_power_curve(wind_speeds, hub_height, roughness_length, csv_file):
    # CSV-Datei einlesen
    df = pd.read_csv(csv_file, delimiter=";")

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

    # Windgeschwindigkeit anpassen
    adjusted_wind_speeds = adjust_wind_speed(wind_speeds, hub_height, roughness_length)

    # Leistung für angepasste Windgeschwindigkeiten berechnen
    power_outputs = fitted_function(adjusted_wind_speeds)

    return power_outputs
