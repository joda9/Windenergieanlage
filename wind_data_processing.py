import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

"""
In diesem Modul befinden sich die Funktionen für die Verarbeitung der Winddaten.
"""

def adjust_wind_speed(wind_speed, hub_height, roughness_length):
    adjusted_speed = wind_speed * (np.log(hub_height / roughness_length) / np.log(10 / roughness_length))
    return adjusted_speed

def fit_power_curve(wind_speeds, hub_height, roughness_length, data_tech, turbine, data_power_curve):
    
    cut_in = float(data_tech[data_tech.index.str.startswith(turbine)]['Cut-in wind speed:'][0].replace(',','').split()[0])
    cut_out = float(data_tech[data_tech.index.str.startswith(turbine)]['Cut-out wind speed:'][0].replace(',','').split()[0])
    rated_power = float(data_tech[data_tech.index.str.startswith(turbine)]['Rated power:'][0].replace(',','').split()[0])
    rated_wind = float(data_tech[data_tech.index.str.startswith(turbine)]['Rated wind speed:'][0].replace(',','').split()[0])
    # Funktion definieren
    def power_function(wind_speed, cut_in, cut_out, rated_power, rated_wind):
        y = np.zeros_like(wind_speed)
        y = np.where(wind_speed < cut_in, 0, y)
        y = np.where((wind_speed < cut_out) & (wind_speed > rated_wind), rated_power, y)
        y = np.where((wind_speed > cut_in) & (wind_speed < rated_wind), rated_power, y)
        
        y = np.where(wind_speed > cut_out, 0, y)
        
        return y
    power_outputs = power_function(wind_speeds, cut_in, cut_out, rated_power, rated_wind)
    print(power_outputs)
    
    
    
    
    
    
    return power_outputs
