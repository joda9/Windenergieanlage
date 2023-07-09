import pandas as pd
import numpy as np

'''
# Read user input for P_min and specify the data type of the 'Mindestleistung' column as float
user_input = pd.read_csv("C:/Users/huliy/Desktop/Windprojekt/Windenergieanlage/data/Usereingaben.csv", delimiter=';', dtype={"Mindestleistung": float})
p_min = user_input["Mindestleistung"].values[0]
'''

#Bespiel
p_min = 2
single_cell_energy = 5120 / 1000
single_cell_cost = 1700

# Read hourly power output data from an Excel file and specify the data type as string
power_data_path = "data/Wetterdaten_Wanna_Szenario_1.xlsx"
tech_infos_path = "data/technical_information.xlsx"
power_df = pd.read_excel(power_data_path)
df_tech_infos = pd.read_excel(tech_infos_path)

# Convert the date-time column to string format
power_df = power_df.applymap(str)


# Extract the turbine names
start_col_index = 9  # The 9th column corresponds to the ACSA A27/225 turbine model
turbine_names = power_df.iloc[:, start_col_index:].columns.values.tolist()

# Extract the power output data
power_outputs = power_df.iloc[:, start_col_index:].values

# Convert power output data to float
power_df.iloc[:, start_col_index:] = power_df.iloc[:, start_col_index:].astype(float)


def calculate_flauten_time(power_df, p_min, output):
    max_flauten_duration = []
    output = output.set_index('Turbine')
    output['max Flauten time'] = {}
    for turbine in power_df.columns[8:]:
        power = power_df[turbine]
        # Find the calm wind duration for each turbine
        calm_wind_duration = []
        current_duration = 0

        for p in power.astype(float):
            if p < p_min / 2:
                current_duration += 1
            else:
                calm_wind_duration.append(current_duration)
                current_duration = 0

        # Append the last calm wind duration if it extends until the end
        if current_duration > 0:
            calm_wind_duration.append(current_duration)

       # Add the last calm wind duration if it extends until the end
        if calm_wind_duration:
            max_flauten_duration.append(max(calm_wind_duration))
            output.loc[turbine]['max Flauten time'] = max(calm_wind_duration)
    
    return output

'''
The calculate_battery_capacity function calculates the total battery capacity based on the longest calm wind duration of each Turbine and minimum power (p_min).
The battery capacity values are stored in a list.
'''
def calculate_battery_capacity(output, p_min):
    output['Battery Capacity'] = {}
    output['Battery Capacity'] = output['max Flauten time'] * p_min
    

    return output

'''
The calculate_soc function calculates the State of Charge (SOC) based on the power output, p_min, and battery capacity. The SOC values are stored in a list.
'''
def calculate_soc(power_outputs, p_min, battery_capacity_list):
    soc_values_list = []

    for power, capacity in zip(power_outputs, battery_capacity_list):
        discharge_efficiency = 0.9  # Assuming discharge efficiency
        charge_efficiency = 0.99  # Assuming charge efficiency

        soc = 100.0  # Initial SOC set to 100%
        soc_values = []

        for p in power:
            energy_out_hour = min(p, p_min)
            energy_in_hour = max(p, p_min) - p_min

            soc -= (energy_out_hour / (capacity * discharge_efficiency)) * 100
            soc += (energy_in_hour / (capacity * charge_efficiency)) * 100

            # SOC should be maintained between 0% and 100%
            soc = np.clip(soc, 0, 100)
            soc_values.append(soc)

        soc_values_list.append(soc_values)

    return soc_values_list


# Calculate the maximum calm wind duration
df_tech_infos = calculate_flauten_time(power_df, p_min, df_tech_infos)

# Calculate the total required battery capacity
df_tech_infos = calculate_battery_capacity(df_tech_infos, p_min)

# Calculate required number of batteries 
df_tech_infos['number of batteries'] = df_tech_infos['Battery Capacity'] / single_cell_energy

# Calculate total cost of batteries 
df_tech_infos['battery cost'] = df_tech_infos['number of batteries'] * single_cell_cost

# Calculate SOC changes
soc_values_list = calculate_soc(power_outputs, p_min, battery_capacity)

# Find the lowest SOC value for each turbine
lowest_soc_values = [min(soc_values) for soc_values in soc_values_list]



'''
# Print the results
print("Max calm wind duration (hours):", max_flauten_duration)
print("Total required battery capacity (kWh):", battery_capacity)
print("SOC changes:", soc_values)
'''

# Store the results in an Excel file
result_df = pd.DataFrame({"Max. Flautenzeit (h)": max_flauten_duration, 
                          "Erforderliche Speicherkapazität (kWh)": battery_capacity, 
                          "Anzahl der Batterien": battery_number,
                          "Btterie Kosten (€)": battery_cost,
                          "niedrigster SOC (%)": lowest_soc_values})
# Store the results in an Excel file
output_path = "data/technical_information_new_kopie.xlsx"

# Read the existing results file (if it exists)
existing_results_df = pd.DataFrame()
try:
    existing_results_df = pd.read_excel(output_path)
except FileNotFoundError:
    pass

# Merge the existing results with the new results
merged_results_df = pd.concat([existing_results_df, result_df], axis=1)

# Write the merged results to the output file
merged_results_df.to_excel(output_path, index=False)