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

## Funktion: adjust_wind_speed

Passt die Windgeschwindigkeit anhand der Nabenhöhe und Rauhigkeitslänge an.

Parameter:
- `wind_speed` (float): Windgeschwindigkeit.
- `hub_height` (float): Nabenhöhe der Windenergieanlage.
- `roughness_length` (float): Rauhigkeitslänge.

Rückgabewert:
- `adjusted_speed` (float): Angepasste Windgeschwindigkeit.

Beispielaufruf:
adjusted_speed = adjust_wind_speed(10.0, 80.0, 0.1)
print(adjusted_speed)

## Funktion: fit_power_curve

Passt die Leistungskurve anhand der Windgeschwindigkeiten an.

Parameter:
- `wind_speeds` (Series): Windgeschwindigkeiten.
- `hub_height` (float): Nabenhöhe der Windenergieanlage.
- `roughness_length` (float): Rauhigkeitslänge.
- `data_tech` (DataFrame): Technische Daten der Windenergieanlage.
- `turbine` (str): Name der Turbine.
- `data_power_curve` (DataFrame): Leistungskurve der Windenergieanlage.

Rückgabewert:
- `power_outputs` (list): Liste der Leistungswerte.

Beispielaufruf:
power_outputs = fit_power_curve(wind_speeds, 80.0, 0.1, data_tech, 'Turbine1', data_power_curve)
print(power_outputs)

## Funktion: process_data

Verarbeitet Winddaten und passt die Leistungskurve an.

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
