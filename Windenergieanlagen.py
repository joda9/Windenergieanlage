import matplotlib.pyplot as plt  
import matplotlib.dates as mdates 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
from wind_data_processing import * 

"""
Winddaten sowie technische Daten der Turbinen und Leistungskurven einlesen
Anschließend werden aus den Daten die Leistungen der Turbinen stundengenau ermittelt
"""
data_wind_path = r'data/Wetterdaten_Wanna_Szenario_1.txt'  # Dateipfad zu den Wetterdaten
save_path_powerdata = r'data/Wetterdaten_Wanna_Szenario_1.xlsx'     # Dateipfad zur Speicherung der Daten in einer xlsx
data_power_curve_path = r'data/powercurves_interpolated.csv'  # Dateipfad zur Leistungskurve
data_tech_path = r'data/technical_information.xlsx'  # Dateipfad zu den technischen Daten

# hub_height = 80.0  # Nabenhöhe der Windenergieanlage
roughness_length = 0.1  # Rauhigkeitslänge

data_wind = process_data(data_wind_path, data_power_curve_path, data_tech_path, save_path_powerdata, roughness_length)
data_wind.to_excel(save_path_powerdata)
# Verarbeitung der Winddaten und Anpassung der Leistungskurve



"""

"""

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
