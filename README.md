# Ertragsberechnung und LCOE von Kleinwindenergieanlagen

Kopiere dir den repository lokal mit

`git clone https://github.com/joda9/Windenergieanlage.git`

Damit eine neue virtuelle Umgebung aufgesetzt wird geh zunächst in den Ordner Windenergieanlage

`cd Windenergieanlage`

Führe folgenden Befehl aus, um die virtuelle Umgebung zu erstellen.

`conda env create -f environment.yml`

Anschließend die virtuelle Umgebung aktivieren mit:

`conda activate WEA`

# Vorverarbeitung von Leistungskurven

Zunächst werden die Daten aus der Datenbank von eind-turbine-models.com geladen


## Funktion: add_website_titles

Fügt den Titel der Webseite sowie zu jeder Turbine die technischen Informationen zu einem DataFrame hinzu.

Parameter:
- df (DataFrame): DataFrame mit den Webseiten-Links.

Rückgabewert:
- DataFrame: DataFrame mit dem hinzugefügten Titel und technischen Infos.

Beispielaufruf:
df = pd.DataFrame({'Links': ['https://example.com/turbine1', 'https://example.com/turbine2']})
df_with_tech_infos = add_website_titles(df)
print(df_with_tech_infos)


## Funktion: preprocess_power_curves

Vorverarbeitet Leistungskurven-Daten durch Erweiterung des Index, Interpolation fehlender Werte und Speichern der vorverarbeiteten Daten in einer neuen Datei.

Parameter:
- `input_file` (str): Pfad zur Eingabedatei mit den Leistungskurven-Daten.
- `output_file` (str): Pfad zur Ausgabedatei zum Speichern der vorverarbeiteten Daten.

Beispielaufruf:
preprocess_power_curves('input.csv', 'output.csv')

# Verarbeitung der Wind- und Leistungsdaten für einen Standort 
## Funktion: process_data

Verarbeitet stündliche Winddaten und fügt für jede Turbine eine Leistung für die entsprechende Windgeschwindigkeit hinzu

Parameter:
- `data_wind_path` (str): Dateipfad zu den Wetterdaten.
- `data_power_curve_path` (str): Dateipfad zur Leistungskurve.
- `data_tech_path` (str): Dateipfad zu den technischen Daten.
- `save_path_powerdata` (str): Speicherpfad für die verarbeiteten Winddaten.
- `hub_height` (float): Nabenhöhe der Windenergieanlage.
- `roughness_length` (float): Rauhigkeitslänge.

Rückgabewert:
- `data_wind` (DataFrame): Verarbeitete Winddaten.

Beispielaufruf:
data_wind = process_data('wind_data.csv', 'power_curve.csv', 'tech_data.xlsx', 'processed_wind_data.csv', 80.0, 0.1)
print(data_wind)
