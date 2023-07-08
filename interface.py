import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os
import pandas as pd


"""
In diesem Modul wird der Code für die Benutzer*innenfläche beschrieben.
"""
# Create a tkinter window
window = tk.Tk()

source_wd = 'DWD'
econ_view = "Nein"
# Define function to process the inputs
def process_inputs(): # type: ignore
    global z0, h_mess, h_soll, required_power, file_name, econ_view 

    z0 = float(entry_z0.get())
    h_soll = float(entry_h_soll.get())
    h_mess = float(entry_h_mess.get())
    required_power = float(entry_required_power.get())
 #source_wd = combo_source_wd.get()
    file_name = entry_file_name.get()
    econ_view = combo_econ_view.get()

   
    if z0 < 0:
        messagebox.showerror("Ungültige Eingabe", "Der Wert von z0 muss positiv sein")
        return
    

    if z0 > 2:
        messagebox.showerror("Ungültige Eingabe", "Der Wert von z0 ist zu groß")
        return


    if h_soll < 0:
        messagebox.showerror("Ungültige Eingabe", "Der Wert der gewünschten Höhe muss positiv sein.")
        return

    if h_mess < 0:
        messagebox.showerror("Ungültige Eingabe", "Der Wert der Messhöhe muss positiv sein.")
        return

    if required_power < 0 or required_power > 250:
        messagebox.showerror("Ungültige Eingabe", "Die gewünschte Leistung muss zwischen 0 und 250 kW liegen.")
        return

    if not z0 or not h_soll or not h_mess or not required_power or not source_wd or not file_name or not econ_view:
        messagebox.showerror("Unvollständige Eingabe", "Bitte alle Felder ausfüllen.")
        return

    try:
        z0 = float(z0)
        h_soll = float(h_soll)
        h_mess = float(h_mess)
        required_power = float(required_power)

    except ValueError:
        messagebox.showerror("Ungültige Eingabe", "Bitte korrekte Werte eintragen.")
        return

    # Check if the file exists
    if not os.path.isfile(file_name):
        messagebox.showerror("Datei nicht gefunden", "Die Datei wurde im Verzeichnis nicht gefunden.")
        return

    window.destroy()  

    values = {
        "z0": z0,
        "h_mess": h_mess,
        "h_soll": h_soll,
        "required_power": required_power,
        "Costs": Costs,
        "interest": interest,
        "duration": duration
    }

    #if source_wd == 'DWD':
    data_wind = pd.read_csv(file_name, delimiter=';')
    data_wind['MESS_DATUM'] = pd.to_datetime(data_wind['MESS_DATUM'], format='%Y%m%d%H')
    data_wind = data_wind.rename(columns={"STATIONS_ID": "StationID", "   F": "F", "   D": "D"})
    #elif source_wd == 'Global Wind Atlas':
    #    data_wind = pd.read_csv(file_name, delimiter=',')
    #    data_wind['MESS_DATUM'] = pd.to_datetime(data_wind['MESS_DATUM'], format='%Y%m%d%H')
    #    data_wind = data_wind.rename(columns={"STATIONS_ID": "StationID", "   F": "F", "   D": "D"})

    return values, data_wind


# Create labels and entry fields for inputs
label_z0 = tk.Label(window, text="z0 (Rauhigkeitslänge)[m]:")
label_z0.pack()
entry_z0 = tk.Entry(window)
entry_z0.pack()

label_h_mess = tk.Label(window, text="Messhöhe[m]:")
label_h_mess.pack()
entry_h_mess = tk.Entry(window)
entry_h_mess.pack()

label_h_soll = tk.Label(window, text="Gewünschte Höhe[m]:")
label_h_soll.pack()
entry_h_soll = tk.Entry(window)
entry_h_soll.pack()

label_required_power = tk.Label(window, text="Gewünschte Leistung[kW]:")
label_required_power.pack()
entry_required_power = tk.Entry(window)
entry_required_power.pack()

# Create a dropdown menu for source_wd

label_file_name = tk.Label(window, text="Name der Wetterdatei:")
label_file_name.pack()
entry_file_name = tk.Entry(window)
entry_file_name.pack()

#label_source_wd = tk.Label(window, text="Choose Weather Datasource:")
#label_source_wd.pack()
#combo_source_wd = ttk.Combobox(window, values=["DWD","Global Wind Atlas", "Renewables.ninja"])
#combo_source_wd.pack()

label_econ_view = tk.Label(window, text="Ökonomische Betrachtung gewünscht?:")
label_econ_view.pack()
combo_econ_view = ttk.Combobox(window, values=["Ja","Nein"])
combo_econ_view.pack()

# Create a button to submit the inputs
submit_button = tk.Button(window, text="Eingabe", command=process_inputs)
submit_button.pack()

# Check if the window is closed without entering data
window.protocol("WM_DELETE_WINDOW",
                lambda: messagebox.showerror("Fehlende Eingabe", "Bitte alle Felder ausfüllen."))

# Run the tkinter event loop
window.mainloop()

#Second layer of a window in case an economic view is necessary 
if econ_view == "Ja":
        window = tk.Tk()
        def process_inputs():
            global Costs, interest, duration
            Costs = float(entry_Costs.get())
            interest = float(entry_interest.get())
            duration = float(entry_duration.get())

            if Costs < 0:
                messagebox.showerror("Ungültige Eingabe", "Kosten müssen positiv sein.")
                return

            if interest < 0:
                messagebox.showerror("Ungültige Eingabe", "der Zins muss positiv sein.")
                return

            if duration < 0:
                messagebox.showerror("Ungültige Eingabe", "Planungsdauer muss positiv sein.")
                return
            

            try:
                Costs = float(Costs)
                interest = float(interest)
                duration = float(duration)

            except ValueError:
                messagebox.showerror("Ungültige Eingabe", "Bitte korrekte Werte eintragen.")
                return


            if not Costs or not interest or not duration:
                messagebox.showerror("Fehlende Eingabe", "Bitte alle Felder ausfüllen.")
                return
            
            # Check if the window is closed without entering data
            window.protocol("WM_DELETE_WINDOW",
                lambda: messagebox.showerror("Fehlende Eingabe", "Bitte alle Felder ausfüllen."))


            window.destroy()


        label_Costs = tk.Label(window, text="Kosten[€]:")
        label_Costs.pack()
        entry_Costs = tk.Entry(window)
        entry_Costs.pack()

        label_interest = tk.Label(window, text="Zinssatz[%]:")
        label_interest.pack()
        entry_interest = tk.Entry(window)
        entry_interest.pack()

        label_duration = tk.Label(window, text="Planlebensdauer[a]:")
        label_duration.pack()
        entry_duration = tk.Entry(window)
        entry_duration.pack()

        submit_button = tk.Button(window, text="Submit", command=process_inputs)
        submit_button.pack()

        # Check if the window is closed without entering data
        window.protocol("WM_DELETE_WINDOW",
                lambda: messagebox.showerror("Missing Input", "Please fill in all required fields."))

        # Run the tkinter event loop
        window.mainloop()


# Show a confirmation message
if all((z0, h_soll, h_mess, required_power, source_wd, file_name, econ_view)):
    messagebox.showinfo("Eingabe Erfolgreich", "Variablenwerte wurden eingegeben")



#if source_wd == 'DWD':
    #data_wind = pd.read_csv(r'data/produkt_ff_stunde_20211202_20230430_00125.txt', delimiter=';')
#    data_wind = pd.read_csv(file_name, delimiter=';')
#    data_wind['MESS_DATUM'] = pd.to_datetime(data_wind['MESS_DATUM'], format='%Y%m%d%H')
#    data_wind = data_wind.rename(columns={"STATIONS_ID": "StationID", "   F": "F", "   D": "D"})

#elif source_wd == 'Global Wind Atlas':
#    data_wind = pd.read_csv(file_name, delimiter=',')
#    data_wind['MESS_DATUM'] = pd.to_datetime(data_wind['MESS_DATUM'], format='%Y%m%d%H')
 #   data_wind = data_wind.rename(columns={"STATIONS_ID": "StationID", "   F": "F", "   D": "D"})



