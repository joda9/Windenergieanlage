import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from tqdm import tqdm
import locale
import requests
from bs4 import BeautifulSoup


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


def power_function(wind_speeds, cut_in, cut_out, rated_power, rated_wind, data_power_curve, turbine):
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

def fit_power_curve(wind_speeds, roughness_length, data_tech, turbine, data_power_curve):
    """
    Passt die Leistungskurve anhand der Windgeschwindigkeiten an.
    
    Args:
        wind_speeds (Series): Windgeschwindigkeiten.
        roughness_length (float): Rauhigkeitslänge.
        data_tech (DataFrame): Technische Daten der Windenergieanlage.
        turbine (str): Name der Turbine.
        data_power_curve (DataFrame): Leistungskurve der Windenergieanlage.
    
    Returns:
        list: Liste der Leistungswerte.
    """

    # cut_in = float(data_tech[data_tech.index.str.startswith(turbine)]['Cut-in wind speed:'][0].replace(',','').split()[0])  # Einschaltdrehzahl der Windenergieanlage
    # cut_out = float(data_tech[data_tech.index.str.startswith(turbine)]['Cut-out wind speed:'][0].replace(',','').replace('-','').split()[0])  # Abschaltdrehzahl der Windenergieanlage
    # rated_power = float(data_tech[data_tech.index.str.startswith(turbine)]['Rated power:'][0].replace(',','').split()[0])  # Nennleistung der Windenergieanlage
    # rated_wind = float(data_tech[data_tech.index.str.startswith(turbine)]['Rated wind speed:'][0].replace(',','').split()[0])  # Nennwindgeschwindigkeit der Windenergieanlage
    
    
    cut_in = float(data_tech['Cutin wind speed:'][data_tech.index.str.startswith(turbine)])    # Einschaltdrehzahl der Windenergieanlage
    cut_out = float(data_tech['Cutout wind speed:'][data_tech.index.str.startswith(turbine)])  # Abschaltdrehzahl der Windenergieanlage
    rated_power = float(data_tech['Rated power:'][data_tech.index.str.startswith(turbine)])  # Nennleistung der Windenergieanlage
    rated_wind = float(data_tech['Rated wind speed:'][data_tech.index.str.startswith(turbine)])  # Nennwindgeschwindigkeit der Windenergieanlage
    hub_height = float(data_tech['Hub height:'][data_tech.index.str.startswith(turbine)])  # Nennwindgeschwindigkeit der Windenergieanlage
    
    w = []  # Liste zur Speicherung der angepassten Windgeschwindigkeiten
    for wind in wind_speeds:
        w.append(adjust_wind_speed(wind, hub_height, roughness_length)) # Anpassung der Windgeschwindigkeiten anhand der Nabenhöhe und Rauhigkeitslänge
    

    power_outputs = power_function(wind_speeds, cut_in, cut_out, rated_power, rated_wind, data_power_curve, turbine)
    return power_outputs

def process_data(data_wind_path, data_power_curve_path, data_tech_path, save_path_powerdata, roughness_length):
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
    
    
    result_df = pd.DataFrame(index=data_wind.index)  # Leeres DataFrame zum Speichern der Ergebnisse der Anpassung der Leistungskurve
    for turbine in tqdm(data_power_curve.columns[1:]): # Iteration über jede Turbine in der Leistungskurve
        try:
            result_df[turbine] = fit_power_curve(data_wind['F'], roughness_length, data_tech, turbine, data_power_curve) # Anpassung der Leistungskurve anhand der Windgeschwindigkeiten und Speicherung der Ergebnisse im DataFrame
        except Exception as e:
            print(turbine, ' klappt nicht wegen', e) # Ausgabe einer Fehlermeldung, falls ein Fehler auftritt

    data_wind = pd.concat([data_wind, result_df], axis=1) # Zusammenführen der verarbeiteten Winddaten mit den Ergebnissen der Leistungskurve
    return data_wind # Rückgabe der verarbeiteten Winddaten




def read_website_information(url):
    """
    Liest die technischen Informationen von einer Webseite aus.

    Args:
        url (str): URL der Webseite.

    Returns:
        DataFrame: DataFrame mit den technischen Informationen.
    """
    # HTTP-Anfrage senden und den HTML-Inhalt erhalten
    response = requests.get(url)  # Senden einer HTTP-Anfrage an die angegebene URL
    html_content = response.content  # Abrufen des Inhalts der Antwort

    # BeautifulSoup verwenden, um den HTML-Inhalt zu analysieren
    soup = BeautifulSoup(html_content, "html.parser")  # Erstellen eines BeautifulSoup-Objekts zum Analysieren des HTML-Inhalts

    # Den Titel der Website extrahieren
    title = soup.title.string
    
    # Alle TabContent finden
    tab_contents = soup.find_all("div", {"class": "TabContent"})  # Finden aller Elemente mit dem Tag "div" und der Klasse "TabContent"

    if tab_contents:
        # Leeres DataFrame erstellen
        df = pd.DataFrame()  # Erstellen eines leeren Pandas DataFrame

        # Durch die Tabellen iterieren
        for tab_content in tab_contents:
            # Datenzeilen extrahieren
            rows = tab_content.find_all("div", {"class": "row"})  # Finden aller Elemente mit dem Tag "div" und der Klasse "row"

            # Leeres DataFrame erstellen
            data = []

            # Durch die Datenzeilen iterieren und Werte extrahieren
            for row in rows:
                left_col = row.find("div", {"class": "col-left"}).text.strip()  # Extrahieren des Texts aus dem Elements mit der Klasse "col-left"
                right_col = row.find("div", {"class": "col-right"}).text.strip()  # Extrahieren des Texts aus dem Elements mit der Klasse "col-right"
                data.append([left_col, right_col])  # Hinzufügen der Werte zur Datenliste

            # DataFrame erstellen
            temp_df = pd.DataFrame(data, columns=['Property', "Value"]).set_index(['Property'])  # Erstellen eines temporären DataFrames mit den extrahierten Werten
            # Das aktuelle DataFrame an das Gesamt-DataFrame anhängen
            df = pd.concat([df, temp_df])  # Zusammenführen des temporären DataFrames mit dem Gesamt-DataFrame

        # Doppelte Spalten entfernen
        df1 = df.drop_duplicates(keep='first')  # Entfernen von doppelten Spalten aus dem DataFrame, wobei die erste Instanz beibehalten wird
        # Nur die erste Instanz der doppelten Spalte behalten
        df1 = df1[~df1.index.duplicated(keep='first')]  # Entfernen von doppelten Zeilen aus dem DataFrame, wobei die erste Instanz beibehalten wird
        df1 = df1.set_index(df1.index).transpose()  # Transponieren des DataFrames und Setzen der Indexspalte als Spaltennamen
        return df1, title  # Rückgabe des vorverarbeiteten DataFrames
    else:
        print("Keine TabContents gefunden.")  # Ausgabe einer Fehlermeldung, wenn keine Tabelleninhalte gefunden wurden




def add_website_infos(df):
    """
    Fügt den Titel der Webseite sowie zu jeder Turbine die technischen Informationen zu einem DataFrame hinzu.

    Args:
        df (DataFrame): DataFrame mit den Webseiten-Links.

    Returns:
        DataFrame: DataFrame mit dem hinzugefügten Titel und technischen Infos.
    """
    # Neue Spalte "Turbine" zum DataFrame hinzufügen
    df["Turbine"] = ""  # Hinzufügen einer leeren Spalte mit dem Namen "Turbine" zum DataFrame

    # Alle Links im DataFrame durchgehen
    df_technical_infos = pd.read_excel('data/technical_information.xlsx')  # Einlesen der technischen Informationen aus einer Excel-Datei

    if not ('check' in df_technical_infos.columns):  # Überprüfen, ob die Spalte "check" im DataFrame vorhanden ist
        df_technical_infos['check'] = np.nan  # Hinzufügen einer neuen Spalte "check" mit NaN-Werten zum DataFrame

    counter = 0  # Initialisieren des Zählers
    progress_bar = tqdm(total=len(df), desc="Progress")  # Erstellen einer Fortschrittsanzeige

    while (counter / (len(df) - 1) < 1):  # Schleife, die solange läuft, bis alle Links verarbeitet wurden
        counter = 0  # Zurücksetzen des Zählers

        for index, row in df_technical_infos.iterrows():  # Iteration über jede Zeile im DataFrame
            if np.isnan(df_technical_infos['check'][index]):  # Überprüfen, ob die "check"-Spalte für den aktuellen Link NaN ist
                try:
                    link = row["Links"]  # Extrahieren des Links aus der aktuellen Zeile


                    # Technische Informationen abrufen
                    tech_infos, title = read_website_information(link)  # Aufrufen der Funktion "read_technical_information", um die technischen Informationen der Webseite zu erhalten

                    for column in tech_infos:  # Iteration über jede Spalte in den technischen Informationen
                        df_technical_infos.at[index, column] = tech_infos[column]['Value']  # Aktualisieren der entsprechenden Zelle im DataFrame mit dem Wert aus den technischen Informationen

                    df_technical_infos.at[index, 'check'] = 1  # Aktualisieren der "check"-Spalte auf 1, um anzuzeigen, dass der Link verarbeitet wurde

                    # Den Titel in die entsprechende Zeile des DataFrames einfügen
                    df_technical_infos.at[index, "Turbine"] = title  # Hinzufügen des Titels in die "Turbine"-Spalte des DataFrames

                    df_technical_infos.to_excel('data/technical_information.xlsx')  # Speichern des aktualisierten DataFrames in einer Excel-Datei
                    progress_bar.update(1)  # Aktualisieren der Fortschrittsanzeige um 1
                except Exception as e:
                    print(e)  # Ausgabe einer Fehlermeldung, falls ein Fehler auftritt
            else:
                progress_bar.update(1)  # Aktualisieren der Fortschrittsanzeige um 1
                counter += 1  # Inkrementieren des Zählers

    return df_technical_infos  # Rückgabe des DataFrames mit den hinzugefügten Titeln
