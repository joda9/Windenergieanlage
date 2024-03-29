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
p_req, roughness_length, p_min, single_cell_energy, single_cell_cost, interest_rate, lifetime, capex, save_path_powerdata, data_power_curve_path, data_tech_path, data_wind_path = get_user_values()

"""
stündliche Leistungsdaten berechnen
"""

data_wind = process_data(data_wind_path, data_power_curve_path, data_tech_path, save_path_powerdata, roughness_length)

# Speichern der Turbinen mit einer Leistung > 45000 kWh für plots
#data_wind_red = data_wind.copy()
#Turbines_bigger_45kWh = data_wind_red.iloc[:, 8:].cumsum(axis=0).columns[(data_wind_red.iloc[:, 8:].cumsum(axis=0).iloc[-1, :] >= 45000)].tolist()

#Speichern der Leistungstabelle



"""
Batteriedimensionierung
"""
tech_battery = calculate_battery_cost(p_min, single_cell_energy, single_cell_cost, data_tech_path, save_path_powerdata)
tech_battery.to_excel(data_tech_path)

"""
LCOE berechnen
"""

tech_lcoe = append_costs_df(capex, lifetime, interest_rate)
tech_lcoe.to_excel(data_tech_path)

"""
Plots
"""

plot_all(data_tech_path, save_path_powerdata, p_req, nr_of_top=15)



