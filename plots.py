import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from windrose import WindroseAxes
from scipy.stats import weibull_min

def plot_all(data_tech_path, save_path_powerdata, nr_of_top):
    '''
    Dieses Modul beinhaltet die Funktionen für den Plot einer Windrose und der Weibullverteilung
    und Kostenvergleich.
    '''

    #Filtern von Anlagen kleiner als 45MWh im Jahr
    data_wind_red = pd.read_excel(save_path_powerdata)
    Turbines_bigger_45kWh = data_wind_red.iloc[:, 8:].cumsum(axis=0).columns[(data_wind_red.iloc[:, 8:].cumsum(axis=0).iloc[-1, :] >= 45000)].tolist()

    #Erstellen von sortierten dfs für die plots
    cost_data_raw = pd.read_excel(data_tech_path).set_index('Turbine')
    cost_data_45kW_raw = cost_data_raw.copy()

    cost_data = cost_data_raw.copy()
    cost_data_45kW = cost_data_45kW_raw.copy().loc[Turbines_bigger_45kWh]

    lcoe_data = cost_data_raw.copy().sort_values('LCOE').head(nr_of_top)
    lcoe_data_45kW = cost_data_45kW_raw.copy().loc[Turbines_bigger_45kWh].sort_values('LCOE').head(nr_of_top)

    turbine_names = lcoe_data.index
    turbine_names_45kW = lcoe_data_45kW.index

    lcoe_values = lcoe_data['LCOE']
    lcoe_values_45kW = lcoe_data_45kW['LCOE']

    #plot der LCOE
    plt.figure(figsize=(10, 6))
    plt.bar(turbine_names, lcoe_values)
    plt.xlabel('Kleinwindenergieanlagenmodell')
    plt.ylabel('LCOE in €/kWh')
    plt.title('LCOE')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig('data/LCOE.png')

    plt.figure(figsize=(10, 6))
    plt.bar(turbine_names_45kW, lcoe_values_45kW)
    plt.xlabel('Kleinwindenergieanlagenmodell')
    plt.ylabel('LCOE in €/kWh')
    plt.title('LCOE für Turbinen größer 45MWh')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig('data/LCOE45.png')

    #Erstellung dfs für Gesamt- und Nebenkosten
    cost_data['Rückbaukosten'] = 6548
    cost_data['Investitionskosten'] = cost_data['Gesamtinvestitionskosten'] - 6548 # Abzug des Rückbaus, weil sonst doppelt im Plot

    cost_data['Stacked Costs'] = cost_data['Investitionskosten'] + \
                                          cost_data['Betriebskosten'] + cost_data['battery cost'] + \
                                          cost_data['Rückbaukosten']

    cost_data_Neb=(cost_data['Stacked Costs']-cost_data['Investitionskosten']).sort_values().head(nr_of_top).index
    cost_data_Ges=cost_data.sort_values('Stacked Costs').head(nr_of_top).index

    cost_data_45kW['Rückbaukosten'] = 6548
    cost_data_45kW['Investitionskosten'] = cost_data_45kW['Gesamtinvestitionskosten'] - 6548 # Abzug des Rückbaus, weil sonst doppelt im Plot

    cost_data_45kW['Stacked Costs'] = cost_data_45kW['Investitionskosten'] + \
                                          cost_data_45kW['Betriebskosten'] + cost_data_45kW['battery cost'] + \
                                          cost_data_45kW['Rückbaukosten']

    cost_data_45kW_Neb=(cost_data_45kW['Stacked Costs']-cost_data_45kW['Investitionskosten']).sort_values().head(nr_of_top).index
    cost_data_45kW_Ges=cost_data_45kW.sort_values('Stacked Costs').head(nr_of_top).index

    # Plot für die gestapelten Kosten der KWEA
    plt.figure(figsize=(15, 10))
    plt.bar(cost_data_Ges, cost_data.loc[cost_data_Ges]['Investitionskosten'], label='Investitionskosten')
    plt.bar(cost_data_Ges, cost_data.loc[cost_data_Ges]['Betriebskosten'], bottom=cost_data.loc[cost_data_Ges]['Investitionskosten'], label='Betriebskosten')
    plt.bar(cost_data_Ges, cost_data.loc[cost_data_Ges]['battery cost'], bottom=cost_data.loc[cost_data_Ges]['Investitionskosten'] + cost_data.loc[cost_data_Ges]['Betriebskosten'], label='Batteriekosten')
    plt.bar(cost_data_Ges, cost_data.loc[cost_data_Ges]['Rückbaukosten'], bottom=cost_data.loc[cost_data_Ges]['Stacked Costs'] - cost_data.loc[cost_data_Ges]['Rückbaukosten'], label='Rückbau')
    plt.xlabel('Kleinwindenergieanlagenmodell')
    plt.ylabel('Gesamtkosten in €')
    plt.title('Gesamtkostenvergleich der Kleinwindenergieanlagen')
    plt.legend()
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig('data/Gesamtinvestitionskosten.png')

    # Plot für die gestapelten Kosten der KWEA
    plt.figure(figsize=(15, 10))
    plt.bar(cost_data_45kW_Ges, cost_data_45kW.loc[cost_data_45kW_Ges]['Investitionskosten'], label='Investitionskosten')
    plt.bar(cost_data_45kW_Ges, cost_data_45kW.loc[cost_data_45kW_Ges]['Betriebskosten'], bottom=cost_data_45kW.loc[cost_data_45kW_Ges]['Investitionskosten'], label='Betriebskosten')
    plt.bar(cost_data_45kW_Ges, cost_data_45kW.loc[cost_data_45kW_Ges]['battery cost'], bottom=cost_data_45kW.loc[cost_data_45kW_Ges]['Investitionskosten'] + cost_data_45kW.loc[cost_data_45kW_Ges]['Betriebskosten'], label='Batteriekosten')
    plt.bar(cost_data_45kW_Ges, cost_data_45kW.loc[cost_data_45kW_Ges]['Rückbaukosten'], bottom=cost_data_45kW.loc[cost_data_45kW_Ges]['Stacked Costs'] - cost_data_45kW.loc[cost_data_45kW_Ges]['Rückbaukosten'], label='Rückbau')
    plt.xlabel('Kleinwindenergieanlagenmodell')
    plt.ylabel('Gesamtkosten in €')
    plt.title('Gesamtkostenvergleich der Kleinwindenergieanlagen größer 45MWh')
    plt.legend()
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig('data/Gesamtinvestitionskosten45.png')

    # Plot für die Nebenkosten und Rückbau einer KWEA.
    plt.figure(figsize=(15, 10))
    plt.bar(cost_data_Neb, cost_data.loc[cost_data_Neb]['Betriebskosten'], label='Betriebskosten', color='green')
    plt.bar(cost_data_Neb, cost_data.loc[cost_data_Neb]['battery cost'], bottom=cost_data.loc[cost_data_Neb]['Betriebskosten'], label='Batteriekosten', color='orange')
    plt.bar(cost_data_Neb, cost_data.loc[cost_data_Neb]['Rückbaukosten'], bottom=cost_data.loc[cost_data_Neb]['Betriebskosten'] + cost_data.loc[cost_data_Neb]['battery cost'], label='Rückbaukosten', color='red')
    plt.xlabel('Kleinwindenergieanlagenmodell')
    plt.ylabel('Nebenkosten in €')
    plt.title('Nebenkostenvergleich der Kleinwindenergieanlagen')
    plt.legend()
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig('data/Nebenkosten.png')

    # Plot für die Nebenkosten und Rückbau einer KWEA.
    plt.figure(figsize=(15, 10))
    plt.bar(cost_data_45kW_Neb, cost_data_45kW.loc[cost_data_45kW_Neb]['Betriebskosten'], label='Betriebskosten', color='green')
    plt.bar(cost_data_45kW_Neb, cost_data_45kW.loc[cost_data_45kW_Neb]['battery cost'], bottom=cost_data_45kW.loc[cost_data_45kW_Neb]['Betriebskosten'], label='Batteriekosten', color='orange')
    plt.bar(cost_data_45kW_Neb, cost_data_45kW.loc[cost_data_45kW_Neb]['Rückbaukosten'], bottom=cost_data_45kW.loc[cost_data_45kW_Neb]['Betriebskosten'] + cost_data_45kW.loc[cost_data_45kW_Neb]['battery cost'], label='Rückbaukosten', color='red')
    plt.xlabel('Kleinwindenergieanlagenmodell')
    plt.ylabel('Nebenkosten in €')
    plt.title('Nebenkostenvergleich der Kleinwindenergieanlagen größer 45MWh')
    plt.legend()
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig('data/Nebenkosten45.png')

    # Plot der LCOE über die Nabenhöhe der KWEA. Macht nur dann Sinn wenn wir von einer KWEA unterschiedliche Nabenhöhen haben
    data_hub_sorted = cost_data.sort_values('Hub height:')
    plt.figure(figsize=(10, 6))
    plt.plot(data_hub_sorted['Hub height:'], data_hub_sorted['LCOE'], marker='o', linestyle='', color='orange')
    plt.xlabel('Nabenhöhe in m')
    plt.ylabel('LCOE in €/kWh')
    plt.title('LCOE über die Nabenhöhe von KWEA')
    plt.grid(True)

    # Winddaten einlesen
    data_wind = pd.read_csv(r'weatherdata/Wetterdaten_Wanna_Szenario_1.txt', delimiter=';')
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

    # Weibull Verteilung plotten:

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
    
    lcoe_data = cost_data.sort_values('LCOE')
    lcoe_data = lcoe_data.head(nr_of_top)
    
    turbine_names = lcoe_data.index
    lcoe_values = lcoe_data['LCOE']
    
    plt.figure(figsize=(10, 6))
    plt.bar(turbine_names, lcoe_values)
    plt.xlabel('Kleinwindenergieanlagenmodell')
    plt.ylabel('LCOE in €/kWh')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig('data/LCOE.png')

    print('Weibull-Verteilungsfaktoren:')
    print('Formfaktor (Shape):', shape)
    print('Lagefaktor (Location):',(loc))
    print('Skalenfaktor (Scale):', scale)

