# Ertragsberechnung und LCOE von Kleinwindenergieanlagen

Kopiere dir den repository lokal mit

`git clone https://github.com/joda9/Windenergieanlage.git`

Damit eine neue virtuelle Umgebung aufgesetzt wird geh zunächst in den Ordner Windenergieanlage

`cd Windenergieanlage`

Führe folgenden Befehl aus, um die virtuelle Umgebung zu erstellen.

`conda env create -f environment.yml`

Anschließend die virtuelle Umgebung aktivieren mit:

`conda activate WEA`

# (nur für Spyder):


Um das Paket spyder-kernels zu installieren, führen Sie den folgenden Befehl aus:

    Für Conda/Anaconda: conda install spyder-kernels

    Für Pip/Virtualenv: pip install spyder-kernels

Nach der Installation führen Sie den folgenden Befehl in derselben Umgebung aus:

python -c "import sys; print(sys.executable)"

Kopieren Sie den zurückgegebenen Pfad (er sollte mit "python", "pythonw", "python.exe" oder "pythonw.exe" enden), indem Sie ihn markieren und kopieren.

Deaktivieren Sie die aktuelle Umgebung und aktivieren Sie die Umgebung, in der Spyder installiert ist (falls Sie es in einer eigenen Umgebung installiert haben). Starten Sie Spyder wie gewohnt.

Nachdem Spyder gestartet ist, navigieren Sie zu Einstellungen > Python-Interpreter > Folgenden Interpreter verwenden und fügen Sie den in Schritt 3 kopierten Pfad in das Textfeld ein.

Starten Sie eine neue IPython-Konsole. Alle Pakete, die in Ihrer Umgebung installiert sind, sollten dort verfügbar sein. Wenn Conda verwendet wird, sollte der Name der aktuellen Umgebung und deren Python-Version in der Statusleiste von Spyder angezeigt werden. Wenn Sie mit der Maus darüber fahren, wird der Pfad des ausgewählten Interpreters angezeigt.

# Vorverarbeitung von Leistungskurven

Zunächst werden die Daten aus der Datenbank von https://wind-turbine-models.com geladen


## Funktion: add_website_infos

Fügt den Titel der Webseite sowie zu jeder Turbine die technischen Informationen zu einem DataFrame hinzu.

Parameter:
- df (DataFrame): DataFrame mit den Webseiten-Links.

Rückgabewert:
- DataFrame: DataFrame mit dem hinzugefügten Titel und technischen Infos.

Beispielaufruf:
df = pd.DataFrame({'Links': ['https://example.com/turbine1', 'https://example.com/turbine2']})
df_with_tech_infos = add_website_infos(df)
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
