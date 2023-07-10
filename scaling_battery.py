
import pandas as pd
import numpy as np

def calculate_flauten_time(power_df, p_min, df_tech_infos):
    """
    Berechnet die längste windstille Dauer und Flautenzeit für jede Turbine.
    
    Args:
        power_df (DataFrame): DataFrame mit den Leistungsdaten.
        p_min (float): Mindestleistung.
        df_tech_infos (DataFrame): DataFrame mit den technischen Informationen.
    
    Returns:
        DataFrame: DataFrame mit den aktualisierten technischen Informationen.
    """
    max_flauten_duration = []
    max_0P = []
    df_tech_infos['max Flauten time'] = {}
    df_tech_infos['Flautenzeit'] = {}
    
    for turbine in power_df.columns[7:]:
        try:
            power = power_df[turbine]
            
            # Find the calm wind duration for each turbine
            calm_wind_duration = []
            no_wind_duration = []
            current_duration = 0
    
            for p in power.astype(float):
                if p < p_min / 2:
                    current_duration += 1
                else:
                    calm_wind_duration.append(current_duration)
                    current_duration = 0
            for p in power.astype(float):
                if p == 0:
                    current_duration += 1
                else:
                    no_wind_duration.append(current_duration)
                    current_duration = 0
    
            # Append the last calm wind duration if it extends until the end
            if current_duration > 0:
                calm_wind_duration.append(current_duration)
    
           # Add the last calm wind duration if it extends until the end
            if calm_wind_duration:
                max_flauten_duration.append(max(calm_wind_duration))
                df_tech_infos['max Flauten time'][turbine] = max(calm_wind_duration)
            if no_wind_duration:
                df_tech_infos['Flautenzeit'][turbine] = max(no_wind_duration)
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



def calculate_battery_cost(p_min, single_cell_energy, single_cell_cost, data_tech_path):
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
    # Read the power and technical information data
    power_data_path = "data/Wetterdaten_Wanna_Szenario_1.xlsx"
    power_df = pd.read_excel(power_data_path)
    df_tech_infos = pd.read_excel(data_tech_path)
    df_tech_infos = df_tech_infos.set_index('Turbine')

    # Convert the date-time column to string format
    power_df = power_df.applymap(str)

    # Extract the turbine names
    start_col_index = 8
    turbine_names = power_df.iloc[:, start_col_index:].columns.values.tolist()

    # Convert power output data to float
    power_df.iloc[:, start_col_index:] = power_df.iloc[:, start_col_index:].astype(float)

    # Calculate the maximum calm wind duration
    df_tech_infos = calculate_flauten_time(power_df, p_min, df_tech_infos)

    # Calculate the required battery capacity and number of batteries
    df_tech_infos = calculate_battery_capacity(df_tech_infos, p_min, single_cell_energy)

    # Calculate the total cost of batteries
    df_tech_infos['battery cost'] = df_tech_infos['number of batteries'] * single_cell_cost

    return df_tech_infos
