import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from interface import *
from wind_data_processing import *


"""
Daten einlesen und modifizieren.

"""

# Wetterdaten einlesen
data_wind = pd.read_csv(r'data/produkt_ff_stunde_20211202_20230430_00125.txt', delimiter=';')
data_wind['MESS_DATUM'] = pd.to_datetime(data_wind['MESS_DATUM'], format='%Y%m%d%H')
data_wind = data_wind.rename(columns={"STATIONS_ID": "StationID", "   F": "F", "   D": "D"})

# Leistungskurven und technischen Daten der KWEA einlesen
data_power_curve = pd.read_csv(r'data/Leistungskurven.txt', delimiter='\t')
data_wind_tech = pd.read_csv(r'data/Daten_WKA.txt', delimiter='\t')

# Multipliziere data_wind mit den entsprechenden Faktoren für jede Turbine
hub_height = 80.0  # Eingabe kommt aus dem GUI TODO: Verbindung zum GUI herstellen
roughness_length = 0.1  # Eingabe kommt aus dem GUI TODO: Verbindung zum GUI herstellen

#TODO: Datensatz extra einlesen wäre besser, dann in Funktion fit_power_curve()
# Parameter windgeschwindigkeit und Leistung auswähelen

data_wind['Nordex'] = fit_power_curve(data_wind['F'],
                                      hub_height,
                                      roughness_length,
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