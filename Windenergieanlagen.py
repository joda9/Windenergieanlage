import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import importlib
import pandas as pd
#from interface import *



if 'interface' in globals():
    importlib.reload(interface)
else:
    import interface
#    
from interface import z0, h_mess, required_power, data_wind, Costs, interest, duration, h_hub
global z0, h_mess, required_power, data_wind, Costs, interest, duration, h_hub
from wind_data_processing import *


"""
Daten einlesen und modifizieren.
"""

# Leistungskurven und technischen Daten der KWEA einlesen
data_power_curve = pd.read_csv(r'data/Leistungskurven.txt', delimiter='\t')
data_wind_tech = pd.read_csv(r'data/Daten_WKA.txt', delimiter='\t')

data_wind['Nordex'] = fit_power_curve(data_wind['F'],
                                      h_hub,
                                      h_mess,
                                      z0,
                                      'data/Leistungskurve Nordex N29.csv')

# Turbinennamen bereinigen
turbine_list = data_power_curve.columns[1:].str.strip().tolist()

# Funktion zum Aktualisieren des Graphen basierend auf der ausgewählten Turbine TODO: Welcher Graphen ist hier gemeint?
def update_graph():
    selected_turbine = turbine_combo.get()
    if selected_turbine:
        graph.clear()
        graph.plot(data_wind['MESS_DATUM'], data_wind[selected_turbine], label=selected_turbine)

        # Achsenbeschriftungen und Titel hinzufügen
        graph.set_xlabel('Datum und Uhrzeit')
        graph.set_ylabel('Leistung')
        graph.set_title(f'Leistung der Turbine {selected_turbine} über die Zeit')

        # Datumsformat für die x-Achse festlegen
        date_format = "%d-%b-%Y %H:%M"
        graph.xaxis.set_major_formatter(mdates.DateFormatter(date_format))

        # Automatische Anpassung des Layouts
        graph.figure.autofmt_xdate()

        # Legende anzeigen
        graph.legend()

        # Graph anzeigen
        canvas.draw()

# GUI erstellen
root = tk.Tk()
root.title("Leistung der Turbine über die Zeit")

# Graph erstellen
fig = plt.figure(figsize=(8, 6))
graph = fig.add_subplot(1, 1, 1)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()


# Frame erstellen
frame = ttk.Frame(root)
frame.pack(pady=10)

# Dropdown-Menü für Turbinenauswahl erstellen
turbine_label = ttk.Label(frame, text="Turbine auswählen:")
turbine_label.pack(side="left", padx=5)
turbine_combo = ttk.Combobox(frame, values=turbine_list, state="readonly")
turbine_combo.pack(side="left", padx=5)
turbine_combo.bind("<<ComboboxSelected>>", lambda event: update_graph())

# Initialen Graph anzeigen
update_graph()

# GUI starten
root.mainloop()
