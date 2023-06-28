import pandas as pd

'''
Ich habe die Winddaten und die Daten für die technischen Parameter eingelesen.
Hier kann der Code für die Dimensionierung des Sepeichers aktualisiert werden 
und es soll eine Funktion am Ende sein, welches später nur noch aufgerufen wird.

Die Input Daten hier sollen dann nicht mehr im Modul stehen.
'''

# Winddaten einlesen
data_wind = pd.read_csv(r'data/produkt_ff_stunde_20211202_20230430_00125.txt', delimiter=';')
data_wind['MESS_DATUM'] = pd.to_datetime(data_wind['MESS_DATUM'], format='%Y%m%d%H')
data_wind = data_wind.rename(columns={"STATIONS_ID": "StationID", "   F": "F", "   D": "D"})

# Leistungskurven und technischen Daten der KWEA einlesen
data_power_curve = pd.read_csv(r'data/Leistungskurven.txt', delimiter='\t')
data_wind_tech = pd.read_csv(r'data/Daten_WKA.txt', delimiter='\t')

# Turbinennamen bereinigen
turbine_list = data_power_curve.columns[1:].str.strip().tolist()

# Berechnung der Mindesakkugröße und Bestimmung der Kosten für den Akku
def max_consecutive_no_power(data, turbine_columns, p_min, data_wind_tech):
    """
    Funktion zur Ermittlung der maximalen Zeit, in der hintereinander kein Strom von jeder Windkraftanlage erzeugt wird.
    Die Funktion fügt eine weitere Spalte hinzu, die die benötigte Akkugröße in kWh enthält.

    Args:
        data (DataFrame): DataFrame mit den data_wind.
        turbine_columns (list): Liste der Spalten, die die Windkraftanlagen identifizieren.
        p_min (float): Grenzwert für die Stromerzeugung.

    Returns:
        DataFrame: DataFrame mit der maximalen Zeit, in der hintereinander kein Strom von jeder Windkraftanlage erzeugt wird und der benötigten Akkugröße.
    """
    max_consecutive = {}
    battery_sizes = {}
    Kosten_WEA = {}
    for turbine_column in turbine_columns:
        consecutive_hours = 0
        max_consecutive_hours = 0
        for _, row in data.iterrows():
            if row[turbine_column] <= 0.5 * p_min:  # p_min halbiert, stunde wird nur gezählt, wenn weniger als die hälfte von p_min produziert wird
                consecutive_hours += 1
                if consecutive_hours > max_consecutive_hours:
                    max_consecutive_hours = consecutive_hours
            else:
                consecutive_hours = 0
        max_consecutive[turbine_column] = max_consecutive_hours
        battery_sizes[turbine_column] = max_consecutive_hours * p_min * 1000 #in kWh
        Kosten_WEA[turbine_column] = data_wind_tech[turbine_column][0] * 4000 * 1000 # Nennleistung in MW mal 1000 für kW und mal 3000 für Preis/kW
    max_consecutive_df = pd.DataFrame({'Turbine': list(max_consecutive.keys()), 'MaxConsecutiveHours': list(max_consecutive.values()), 'Battery Size in kWh': list(battery_sizes.values()), 'Kosten WEA': list(Kosten_WEA.values())})
    max_consecutive_df['Kosten_Batterie_Euro'] = max_consecutive_df['Battery Size in kWh'] * 1200

    return max_consecutive_df

#Dummy für mindestleistung
mindestleistung = 100

# Aufrufen der Funktion
p_min = mindestleistung / 1000000 # Grenzwert für die Stromerzeugung in MW
hours_without_power_df = max_consecutive_no_power(data_wind, turbine_list, p_min, data_wind_tech)
hours_without_power_df['Gesamtkosten in T€'] = (hours_without_power_df['Kosten WEA'] + hours_without_power_df['Kosten_Batterie_Euro']) / 1000
hours_without_power_df


def calculate_total_energy(data, turbine_columns):
    """
    Funktion zur Berechnung des Gesamtenergieertrags für jede Windkraftanlage
    über den betrachtetem Zeitraum in MWh.

    Args:
        data (DataFrame): DataFrame mit den data_wind.
        turbine_columns (list): Liste der Spalten, die die Windkraftanlagen identifizieren.

    Returns:
        DataFrame: DataFrame mit dem Gesamtenergieertrag für jede Windkraftanlage.
    """
    total_energy = {}
    for turbine_column in turbine_columns:
        total_energy[turbine_column] = data[turbine_column].sum()

    return pd.DataFrame({'Turbine': list(total_energy.keys()), 'TotalEnergy in MWh': list(total_energy.values())})

# Beispielaufruf der Funktion
total_energy = calculate_total_energy(data_wind, turbine_list)
print(total_energy)