import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os

"""
In diesem Modul wird de Code für die Benutzer*innenfläche beschrieben.
"""
# Create a tkinter window
window = tk.Tk()

# Define function to process the inputs
def process_inputs():
    global alpha, z0, h, required_power, option, file_name
    alpha = float(entry_alpha.get())
    z0 = float(entry_z0.get())
    h = float(entry_h.get())
    required_power = float(entry_required_power.get())
    option = combo_option.get()
    file_name = entry_file_name.get()

    if alpha < 0 or alpha > 2:
        messagebox.showerror("Invalid Input", "Alpha value must be between 0 and 10.")
        return

    if z0 < 0:
        messagebox.showerror("Invalid Input", "z0 value must be positive.")
        return

    if h < 0:
        messagebox.showerror("Invalid Input", "h value must be positive.")
        return

    if required_power < 0 or required_power > 250:
        messagebox.showerror("Invalid Input", "Required power value must be between 0 and 250.")
        return

    if not alpha or not z0 or not h or not required_power or not option or not file_name:
        messagebox.showerror("Missing Input", "Please fill in all required fields.")
        return

    try:
        alpha = float(alpha)
        z0 = float(z0)
        h = float(h)
        required_power = float(required_power)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numeric values.")
        return

    # Check if the file exists
    if not os.path.isfile(file_name):
        messagebox.showerror("File Not Found", "The specified file does not exist in the directory.")
        return

    window.destroy()  # Close the window

    # Continue with the rest of the code
    # ...


# Create labels and entry fields for inputs
label_alpha = tk.Label(window, text="Alpha:")
label_alpha.pack()
entry_alpha = tk.Entry(window)
entry_alpha.pack()

label_z0 = tk.Label(window, text="z0:")
label_z0.pack()
entry_z0 = tk.Entry(window)
entry_z0.pack()

label_h = tk.Label(window, text="h[m]:")
label_h.pack()
entry_h = tk.Entry(window)
entry_h.pack()

label_required_power = tk.Label(window, text="Required Power[kW]:")
label_required_power.pack()
entry_required_power = tk.Entry(window)
entry_required_power.pack()

# Create a dropdown menu for an option

label_file_name = tk.Label(window, text="Enter File Name:")
label_file_name.pack()
entry_file_name = tk.Entry(window)
entry_file_name.pack()

label_option = tk.Label(window, text="Choose Weather Datasource:")
label_option.pack()
combo_option = ttk.Combobox(window, values=["Merra", "Era5", "DWD"])
combo_option.pack()

# Create a button to submit the inputs
submit_button = tk.Button(window, text="Submit", command=process_inputs)
submit_button.pack()

# Check if the window is closed without entering data
window.protocol("WM_DELETE_WINDOW",
                lambda: messagebox.showerror("Missing Input", "Please fill in all required fields."))

# Run the tkinter event loop
window.mainloop()

# Show a confirmation message
if all((alpha, z0, h, required_power, option, file_name)):
    messagebox.showinfo("Input Received", "Variable values have been entered")