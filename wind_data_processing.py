import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from tqdm import tqdm
import locale


def preprocess_power_curves(input_file, output_file):
    """
    Verarbeitet die Leistungskurven-Daten durch Erweiterung des Index, Interpolation von fehlenden Werten
    und speichert die vorverarbeiteten Daten in einer neuen Datei.
    
    Args:
        input_file (str): Pfad zur Eingabedatei mit den Leistungskurven-Daten.
        output_file (str): Pfad zur Ausgabedatei für das Speichern der vorverarbeiteten Daten.
    """
    # Lokales Datumsformat auf Deutsch setzen
    locale.setlocale(locale.LC_TIME, "de_DE.utf8")

    # Leistungskurven-Daten einlesen
    winddaten_df = pd.read_csv(input_file, encoding="ISO-8859-1").set_index(['wind_speed'])

    # Index in 0,01-Schritten bis zu 100 erweitern
    new_index = np.arange(0, 100.01, 0.01)

    # DataFrame neu indexieren und fehlende Werte mit NaN auffüllen
    winddaten_df = winddaten_df.reindex(new_index, fill_value=np.nan)

    # Fehlende Werte mit linearer Interpolation interpolieren
    winddaten_df = winddaten_df.interpolate(method='linear')

    # Verbleibende NaN-Werte mit 0 auffüllen
    winddaten_df_filled = winddaten_df.fillna(0)

    # Vorverarbeitete Daten in eine neue Datei speichern
    winddaten_df_filled.to_csv(output_file)


def adjust_wind_speed(wind_speed, hub_height, roughness_length):
    """
    Passt die Windgeschwindigkeit an die Nabenhöhe und die Rauhigkeitslänge an.
    
    Args:
        wind_speed (float): Windgeschwindigkeit.
        hub_height (float): Nabenhöhe der Windenergieanlage.
        roughness_length (float): Rauhigkeitslänge.
    
    Returns:
        float: Angepasste Windgeschwindigkeit.
    """
    adjusted_speed = np.round(wind_speed * (np.log(hub_height / roughness_length) / np.log(10 / roughness_length)), decimals=1)
    return adjusted_speed

def fit_power_curve(wind_speeds, hub_height, roughness_length, data_tech, turbine, data_power_curve):
    """
    Passt die Leistungskurve anhand der Windgeschwindigkeiten an.
    
    Args:
        wind_speeds (Series): Windgeschwindigkeiten.
        hub_height (float): Nabenhöhe der Windenergieanlage.
        roughness_length (float): Rauhigkeitslänge.
        data_tech (DataFrame): Technische Daten der Windenergieanlage.
        turbine (str): Name der Turbine.
        data_power_curve (DataFrame): Leistungskurve der Windenergieanlage.
    
    Returns:
        list: Liste der Leistungswerte.
    """

    cut_in = float(data_tech[data_tech.index.str.startswith(turbine)]['Cut-in wind speed:'][0].replace(',','').split()[0])  # Einschaltdrehzahl der Windenergieanlage
    cut_out = float(data_tech[data_tech.index.str.startswith(turbine)]['Cut-out wind speed:'][0].replace(',','').replace('-','').split()[0])  # Abschaltdrehzahl der Windenergieanlage
    rated_power = float(data_tech[data_tech.index.str.startswith(turbine)]['Rated power:'][0].replace(',','').split()[0])  # Nennleistung der Windenergieanlage
    rated_wind = float(data_tech[data_tech.index.str.startswith(turbine)]['Rated wind speed:'][0].replace(',','').split()[0])  # Nennwindgeschwindigkeit der Windenergieanlage
    
    def power_function(wind_speeds, cut_in, cut_out, rated_power, rated_wind, data_power_curve):
        """
        Interne Hilfsfunktion zur Berechnung des Leistungswerts.
        
        Args:
            wind_speeds (Series): Windgeschwindigkeiten.
            cut_in (float): Einschaltdrehzahl der Windenergieanlage.
            cut_out (float): Abschaltdrehzahl der Windenergieanlage.
            rated_power (float): Nennleistung der Windenergieanlage.
            rated_wind (float): Nenngeschwindigkeit der Windenergieanlage.
            data_power_curve (DataFrame): Leistungskurve der Windenergieanlage.
        
        Returns:
            list: Liste der Leistungswerte.
        """
        power_values = []  # Liste zur Speicherung der Leistungswerte
        for wind_speed in wind_speeds:
            if wind_speed > cut_out:  # Falls die Windgeschwindigkeit größer als die Abschaltdrehzahl ist
                power_values.append(0)  # Leistungswert ist 0
            elif wind_speed < cut_in :
                # Falls die Windgeschwindigkeit kleiner als die Einschaltdrehzahl ist
                power_values.append(0)  # Leistungswert ist 0
            elif (wind_speed < cut_out and wind_speed > rated_wind):
                # Falls die Windgeschwindigkeit kleiner als die Abschaltdrehzahl und größer als die Nenngeschwindigkeit
                power_values.append(rated_power) # Leistungswert = Nennleistung
            else:
                power = data_power_curve.loc[data_power_curve['wind_speed'] == wind_speed, turbine].values[0] # Leistungswert aus der Leistungskurve abrufen
                power_values.append(power)  # Leistungswert zur Liste hinzufügen
        wind_speeds[turbine] = power_values  # Leistungswerte als neue Spalte zum DataFrame hinzufügen
        return power_values

    power_outputs = power_function(wind_speeds, cut_in, cut_out, rated_power, rated_wind, data_power_curve)
    return power_outputs

def process_data(data_wind_path, data_power_curve_path, data_tech_path, save_path_powerdata, hub_height, roughness_length):
    """
    Verarbeitet die Winddaten und passt die Leistungskurve an.
    
    Args:
        data_wind_path (str): Dateipfad zu den Wetterdaten.
        data_power_curve_path (str): Dateipfad zur Leistungskurve.
        data_tech_path (str): Dateipfad zu den technischen Daten.
        hub_height (float): Nabenhöhe der Windenergieanlage.
        roughness_length (float): Rauhigkeitslänge.
    
    Returns:
        DataFrame: Verarbeitete Winddaten.
    """
    data_wind = pd.read_csv(data_wind_path, delimiter=';')  # Einlesen der Wetterdaten aus einer CSV-Datei
    data_wind['MESS_DATUM'] = pd.to_datetime(data_wind['MESS_DATUM'], format='%Y%m%d%H') # Konvertieren des Datumsformats in ein DateTime-Objekt
    
    data_wind = data_wind.rename(columns={"STATIONS_ID": "StationID", "   F": "F", "   D": "D"}) # Umbenennen der Spaltennamen im DataFrame
    
    data_power_curve = pd.read_csv(data_power_curve_path, encoding="ISO-8859-1")
    data_power_curve = data_power_curve.astype(float)  # Konvertieren der Daten in den float-Datentyp
    data_power_curve['wind_speed'] = data_power_curve['wind_speed'].round(2)  # Runden der Windgeschwindigkeiten auf 2 Dezimalstellen
    
    data_tech = pd.read_excel(data_tech_path, index_col='Turbine') # Einlesen der technischen Daten aus einer Excel-Datei
    
    w = []  # Liste zur Speicherung der angepassten Windgeschwindigkeiten
    for wind in data_wind['F']:
        w.append(adjust_wind_speed(wind, hub_height, roughness_length)) # Anpassung der Windgeschwindigkeiten anhand der Nabenhöhe und Rauhigkeitslänge
    data_wind['true_windspeed'] = w  # Hinzufügen der angepassten Windgeschwindigkeiten als neue Spalte zum DataFrame
    
    result_df = pd.DataFrame(index=data_wind.index)  # Leeres DataFrame zum Speichern der Ergebnisse der Anpassung der Leistungskurve
    for turbine in tqdm(data_power_curve.columns[1:]): # Iteration über jede Turbine in der Leistungskurve
        try:
            result_df[turbine] = fit_power_curve(data_wind['true_windspeed'].copy(), hub_height, roughness_length, data_tech, turbine, data_power_curve) # Anpassung der Leistungskurve anhand der Windgeschwindigkeiten und Speicherung der Ergebnisse im DataFrame
        except Exception as e:
            print(turbine, ' klappt nicht wegen', e) # Ausgabe einer Fehlermeldung, falls ein Fehler auftritt

    data_wind = pd.concat([data_wind, result_df], axis=1) # Zusammenführen der verarbeiteten Winddaten mit den Ergebnissen der Leistungskurve
    return data_wind # Rückgabe der verarbeiteten Winddaten