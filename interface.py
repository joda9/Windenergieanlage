import tkinter as tk
from tkinter import filedialog, messagebox
import os

def get_user_values():
    root = tk.Tk()

    # Funktion zum Speichern der Werte und Beenden der GUI
    def save_values():
        global roughness_length, p_min, single_cell_energy, single_cell_cost, interest_rate, lifetime, capex, save_path_powerdata, data_power_curve_path, data_tech_path, data_wind_path
        roughness_length = float(entry_roughness_length.get())
        p_min = float(entry_p_min.get())
        single_cell_energy = float(entry_single_cell_energy.get())
        single_cell_cost = float(entry_single_cell_cost.get())
        interest_rate = float(entry_interest_rate.get())
        lifetime = int(entry_lifetime.get())
        capex = float(entry_capex.get())
        save_path_powerdata = entry_save_path_powerdata.get()
        data_power_curve_path = var_data_power_curve_path.get()
        data_tech_path = var_data_tech_path.get()
        data_wind_path = var_data_wind_path.get()

        root.destroy()

    root.title("Eingabewerte")
    root.geometry("400x550")  # Vergrößert die Höhe des Fensters

    # Label und Eingabefelder
    label_roughness_length = tk.Label(root, text="Rauhigkeitslänge:")
    label_roughness_length.pack()
    entry_roughness_length = tk.Entry(root)
    entry_roughness_length.insert(tk.END, "0.1")
    entry_roughness_length.pack()

    label_p_min = tk.Label(root, text="p_min (kW):")
    label_p_min.pack()
    entry_p_min = tk.Entry(root)
    entry_p_min.insert(tk.END, "0.300")
    entry_p_min.pack()

    label_single_cell_energy = tk.Label(root, text="Single Cell Energy (kWh):")
    label_single_cell_energy.pack()
    entry_single_cell_energy = tk.Entry(root)
    entry_single_cell_energy.insert(tk.END, str(5120 / 1000))
    entry_single_cell_energy.pack()

    label_single_cell_cost = tk.Label(root, text="Single Cell Cost (€):")
    label_single_cell_cost.pack()
    entry_single_cell_cost = tk.Entry(root)
    entry_single_cell_cost.insert(tk.END, "1700")
    entry_single_cell_cost.pack()

    label_interest_rate = tk.Label(root, text="Interest Rate:")
    label_interest_rate.pack()
    entry_interest_rate = tk.Entry(root)
    entry_interest_rate.insert(tk.END, "0.04")
    entry_interest_rate.pack()

    label_lifetime = tk.Label(root, text="Lifetime (years):")
    label_lifetime.pack()
    entry_lifetime = tk.Entry(root)
    entry_lifetime.insert(tk.END, "20")
    entry_lifetime.pack()

    label_capex = tk.Label(root, text="Capex (€/kW):")
    label_capex.pack()
    entry_capex = tk.Entry(root)
    entry_capex.insert(tk.END, "4500")
    entry_capex.pack()

    label_save_path_powerdata = tk.Label(root, text="Save Path Power Data:")
    label_save_path_powerdata.pack()
    entry_save_path_powerdata = tk.Entry(root)
    entry_save_path_powerdata.insert(tk.END, r'data/Wetterdaten_Wanna_Szenario_1.xlsx')
    entry_save_path_powerdata.pack()

    label_data_power_curve_path = tk.Label(root, text="Data Power Curve Path:")
    label_data_power_curve_path.pack()
    var_data_power_curve_path = tk.StringVar(root)
    data_power_curve_files = [f for f in os.listdir('data') if os.path.isfile(os.path.join('data', f))]
    var_data_power_curve_path.set(data_power_curve_files[0])
    dropdown_data_power_curve_path = tk.OptionMenu(root, var_data_power_curve_path, *data_power_curve_files)
    dropdown_data_power_curve_path.pack()

    label_data_tech_path = tk.Label(root, text="Data Tech Path:")
    label_data_tech_path.pack()
    var_data_tech_path = tk.StringVar(root)
    data_tech_files = [f for f in os.listdir('data') if os.path.isfile(os.path.join('data', f))]
    var_data_tech_path.set(data_tech_files[0])
    dropdown_data_tech_path = tk.OptionMenu(root, var_data_tech_path, *data_tech_files)
    dropdown_data_tech_path.pack()

    label_data_wind_path = tk.Label(root, text="Data Wind Path:")
    label_data_wind_path.pack()
    var_data_wind_path = tk.StringVar(root)
    data_wind_files = [f for f in os.listdir('weatherdata') if os.path.isfile(os.path.join('weatherdata', f))]
    var_data_wind_path.set(data_wind_files[0])
    dropdown_data_wind_path = tk.OptionMenu(root, var_data_wind_path, *data_wind_files)
    dropdown_data_wind_path.pack()

    # Speichern-Button
    button_save = tk.Button(root, text="Speichern", command=save_values)
    button_save.pack()

    root.mainloop()

    # Rückgabe der eingegebenen Werte
    return (
        float(roughness_length),
        float(p_min),
        float(single_cell_energy),
        float(single_cell_cost),
        float(interest_rate),
        int(lifetime),
        float(capex),
        os.path.join(save_path_powerdata),
        os.path.join('data', data_power_curve_path),
        os.path.join('data', data_tech_path),
        os.path.join('weatherdata', data_wind_path)
    )
