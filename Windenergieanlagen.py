import matplotlib.pyplot as plt  
import matplotlib.dates as mdates 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
from wind_data_processing import * 
from calc_lcoe import * 
from scaling_battery import * 
from plots import * 
from interface import *

"""
Winddaten sowie technische Daten der Turbinen und Leistungskurven einlesen
Anschließend werden aus den Daten die Leistungen der Turbinen stundengenau ermittelt
"""


"""
Nutzereingabe
"""
roughness_length, p_per_y, p_min, single_cell_energy, single_cell_cost, interest_rate, lifetime, capex, save_path_powerdata, data_power_curve_path, data_tech_path, data_wind_path = get_user_values()


"""
stündliche Leistungsdaten berechnen
"""
data_wind = process_data(data_wind_path, data_power_curve_path, data_tech_path, save_path_powerdata, roughness_length, p_per_y, lifetime)
data_wind.to_excel(save_path_powerdata)


"""
Batteriedimensionierung
"""
tech_battery = calculate_battery_cost(p_min, single_cell_energy, single_cell_cost, data_tech_path, p_per_y, save_path_powerdata)
tech_battery.to_excel(data_tech_path)

"""
LCOE berechnen
"""
tech_lcoe = append_costs_df(capex, lifetime, interest_rate)
tech_lcoe.to_excel(data_tech_path)

"""
Plots
"""
plot_all(data_tech_path,nr_of_top=15)

