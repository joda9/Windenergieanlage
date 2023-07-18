import pandas as pd
import numpy as np

def calculate_flauten_time(power_df, p_min, df_tech_infos):
    """
    Berechnet die längste windstille Dauer und Flautenzeit für jede Turbine.
    
    Args:
        power_df (DataFrame): DataFrame mit den Leistungsdaten.
        p_min (float): Mindestleistung.
        df_tech_infos (DataFrame): DataFrame mit den technischen Informationen.
    
    Ausgabe:
        DataFrame: DataFrame df_tech_infos mit Spalte, in der die Flautenlänge gespeichert ist.
    """
    #max_0P = []
    df_tech_infos['max Flauten time'] = {}
    df_tech_infos['Flautenzeit'] = {}
    
    for turbine in power_df.columns[7:]:
        try:
            power = power_df[turbine]
            
            # Flautensuche
            calm_wind_duration = []
            no_wind_duration = []
            current_duration = 0
    
            for p in power.astype(float):
                if p < (p_min / 2):
                    current_duration += 1
                else:
                    calm_wind_duration.append(current_duration)
                    current_duration = 0

            # Berücksichtigung Flauten am Ende des Betrachtungszeitraums
            if current_duration > 0:
                calm_wind_duration.append(current_duration)

            for p in power.astype(float):
                if p == 0:
                    current_duration += 1
                else:
                    no_wind_duration.append(current_duration)
                    current_duration = 0
    
            # Berücksichtigung Flauten am Ende des Betrachtungszeitraums
            if current_duration > 0:
                no_wind_duration.append(current_duration)

           # Speichern der längsten Perioden von Flaute und Windstille, sofern sie existieren
            if calm_wind_duration:
                #max_flauten_duration.append(max(calm_wind_duration))
                df_tech_infos.loc[turbine, 'max Flauten time'] = max(calm_wind_duration)
            if no_wind_duration:
                df_tech_infos.loc[turbine, 'Flautenzeit'] = max(calm_wind_duration)

        except Exception as e:
            print(e)
    
    return df_tech_infos


def calculate_battery_capacity(df_tech_infos, p_min, single_cell_energy):
    """
    Berechnet die erforderliche Batteriekapazität und Anzahl der Batterien.
    
    Args:
        df_tech_infos (DataFrame): DataFrame mit den technischen Informationen.
        p_min (float): Mindestleistung.
        single_cell_energy (float): Energiekapazität einer einzelnen Batteriezelle.
    
    Returns:
        DataFrame: DataFrame mit den aktualisierten technischen Informationen.
    """
    df_tech_infos['Battery Capacity'] = df_tech_infos['max Flauten time'] * p_min
    df_tech_infos['Battery Capacity'] = df_tech_infos['Battery Capacity'].fillna(0)  # NaN-Werte mit 0 ersetzen
    df_tech_infos['number of batteries'] = np.ceil(df_tech_infos['Battery Capacity'] / single_cell_energy)
    
    return df_tech_infos




def calculate_battery_cost(p_min, single_cell_energy, single_cell_cost, data_tech_path, save_path_powerdata):

    """
    Berechnet die Batteriekosten basierend auf den gegebenen Parametern.
    
    Args:
        p_min (float): Mindestleistung.
        single_cell_energy (float): Energiekapazität einer einzelnen Batteriezelle.
        single_cell_cost (float): Kosten einer einzelnen Batteriezelle.
        data_tech_path (str): Pfad zur Datei mit den technischen Informationen.
    
    Returns:
        DataFrame: DataFrame mit den aktualisierten technischen Informationen.
    """

    # Einlesen von Leistung und technischen Kennwerten
    power_df = pd.read_excel(save_path_powerdata)
    df_tech_infos = pd.read_excel(data_tech_path)
    df_tech_infos = df_tech_infos.set_index('Turbine')
    #df_tech_infos = pd.read_excel(data_tech_path, index_col=1)

    # Date-Time_Index zu String
    power_df = power_df.applymap(str)

    # Bestimmung Namen der Turbinen
    start_col_index = 8
    turbine_names = power_df.iloc[:, start_col_index:].columns.values.tolist()



    # Umrechnung des Ausgabedateiformats in float
    power_df.iloc[:, start_col_index:] = power_df.iloc[:, start_col_index:].astype(float)

    #for turbine in turbine_names:
    #    if power_df[turbine].sum() < p_per_y:
    #        power_df.drop(turbine, axis='columns', inplace=True)
    #        df_tech_infos.drop(turbine, axis= 'index', inplace=True)


    # Berechnung der maximalen Flautenzeit oder Windstillezeit über den gesamten DataFrame
    df_tech_infos = calculate_flauten_time(power_df, p_min, df_tech_infos)

    # Berechnung der benötigten Batteriekapazität und -Anzahl
    df_tech_infos = calculate_battery_capacity(df_tech_infos, p_min, single_cell_energy)

    # Berechnung der Batteriekosten
    df_tech_infos['battery cost'] = df_tech_infos['number of batteries'] * single_cell_cost

    return df_tech_infos
