import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from windrose import WindroseAxes
from scipy.stats import weibull_min

'''
Dieses Modul beinhaltet die Funktionen für den Plot einer Windrose und der Weibullverteilung
'''

# Winddaten einlesen
data_wind = pd.read_csv(r'data/produkt_ff_stunde_20211202_20230430_00125.txt', delimiter=';')
data_wind['MESS_DATUM'] = pd.to_datetime(data_wind['MESS_DATUM'], format='%Y%m%d%H')
data_wind = data_wind.rename(columns={"STATIONS_ID": "StationID", "   F": "F", "   D": "D"})


# data_wind aus DataFrame lesen
data = data_wind.copy()

# Windrichtungen und Geschwindigkeiten definieren
directions = data['D']
speeds = data['F']

# Werte unter 0 auf NaN setzen
speeds = speeds.copy()
directions = directions.copy()

speeds.loc[speeds < 0] = np.nan
directions.loc[directions < 0] = np.nan

# Windrose plotten
ax = WindroseAxes.from_ax()
ax.bar(directions, speeds, normed=True, opening=0.8, edgecolor='white')
ax.set_legend(title='Häufigkeit (%)')
plt.show()


ax.bar(directions, speeds, normed=True, nsector=16)
table = ax._info["table"]
wd_freq = np.sum(table, axis=0)

direction = ax._info["dir"]
wd_freq = np.sum(table, axis=0)

plt.bar(np.arange(16), wd_freq, align="center")
xlabels = (
    "N", "",
    "N-E", "",
    "E", "",
    "S-E", "",
    "S", "",
    "S-O", "",
    "O", "",
    "N-O", "",
)
xticks = np.arange(16)
plt.gca().set_xticks(xticks)
plt.gca().set_xticklabels(xlabels)
plt.show()



#Weibull Verteilung plotten:

# data_wind aus DataFrame lesen
data = data_wind.copy()

# Windgeschwindigkeiten auslesen
wind_speeds = np.array(data['F'])

# Faktoren für Weibull-Verteilung berechnen
shape, loc, scale = weibull_min.fit(wind_speeds, loc=0)

# Weibull-Verteilung generieren
x = np.linspace(0, wind_speeds.max(), 100)
pdf = weibull_min.pdf(x, shape, loc=loc, scale=scale)

# Histogramm der Windgeschwindigkeiten plotten
plt.hist(wind_speeds, bins=20, density=True, alpha=0.7, label='Windgeschwindigkeiten')

# Weibull-Verteilung plotten
plt.plot(x, pdf, 'r-', lw=2, label='Weibull-Verteilung')

# Diagramm beschriften
plt.xlabel('Windgeschwindigkeit (m/s)')
plt.ylabel('Häufigkeit')
plt.title('Weibull-Verteilung der Windgeschwindigkeiten')
plt.legend()
plt.show()

# Ausgabe der Weibull-Faktoren
print('Weibull-Verteilungsfaktoren:')
print('Formfaktor (Shape):', shape)
print('Lagefaktor (Location):', loc)
print('Skalenfaktor (Scale):', scale)
