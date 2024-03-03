# to show charging conditions in GUI

import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

class BatteryUI:
    
    def __init__(self, root, style, charger_id, row, col,current_soc,required_soc,arrival_time,departure_time,battery_capacity,charging_power,charging_price):
        self.root = root
        # Create a frame for each battery
        style.configure("battery.TFrame", background="#CBC3E3")
        self.frame = ttk.Frame(root, padding="10", style="battery.TFrame")
        self.frame.grid(row=row, column=col, padx=5, pady=5)

        self.charger_id=charger_id
        self.charge_level = (current_soc / 100) * 150 # Set initial charge level (between 0 and 100)//map to 100 with filling the rectangle
        self.required_soc = required_soc
        self.arrival_time = arrival_time
        self. departure_time = departure_time
        self.battery_capacity = battery_capacity
        self.chariging_power = charging_power
        self.charging_price = charging_price
        self.root.configure(background='#CBC3E3') # Change the background color of the root window
        font=("Hack Regular", 10)
        self.canvas = tk.Canvas(self.frame, width=200, height=100, bg="#CBC3E3", highlightthickness=2) # Draw the battery outline
        self.canvas.pack()

        self.canvas.create_rectangle(20, 20, 180, 80, outline="white", width=5) # Draw the battery border
        self.canvas.create_rectangle(180, 35, 195, 65, outline="white", width=5)

        self.battery_fill = self.canvas.create_rectangle(25, 25, 25 + self.charge_level, 75, outline="", fill="green") # Draw the battery fill based on the initial charge level

        self.label_charger_id = ttk.Label(self.frame, text=f"Charger id: {self.charger_id}", background="#CBC3E3", foreground="black", font=font) #Battery id
        self.label_charger_id.pack()
        
        # Create a label to display the charge level
        self.label_charge = ttk.Label(self.frame, text=f"Charge Level: {current_soc}%", background="#CBC3E3", foreground="black", font=font)
        self.label_charge.pack()
        
        #Required charge level
        self.label_required_soc = ttk.Label(self.frame, text=f"Required Charge Level: {self.required_soc}%", background="#CBC3E3",
                                      foreground="black", font=font)
        self.label_required_soc.pack()
             
        # Create a label to display the charge level
        self.label_charge = ttk.Label(self.frame, text=f"Start_Charge Level: {current_soc}%", background="#CBC3E3",
                                      foreground="black", font=font)
        self.label_charge.pack()

        # Create a label to display the arrival_time
        self.label_arrival_time = ttk.Label(self.frame, text=f"Arrival time: {self.arrival_time}", background="#CBC3E3",
                                      foreground="black", font=font)
        self.label_arrival_time.pack()
        
        # Create a label to display the arrival_time
        self.label_arrival_time = ttk.Label(self.frame, text=f"Departure time: {self.departure_time}", background="#CBC3E3",
                                      foreground="black", font=font)
        self.label_arrival_time.pack()

        # Create a label to display the battery capacity 
        self.label_power = ttk.Label(self.frame, text=f"Battery Capacity: {self.battery_capacity}kWh", background="#CBC3E3",
                                     foreground="green", font=font)
        self.label_power.pack()
        
        # Create a label to display the charging power 
        self.label_power = ttk.Label(self.frame, text=f"Charging Power: {self.chariging_power}W", background="#CBC3E3",
                                     foreground="green", font=font)
        self.label_power.pack()

        # Create a label to display the charging price
        self.label_power = ttk.Label(self.frame, text=f"Charging price: ${self.charging_price}", background="#CBC3E3",
                                     foreground="blue", font=font)
        self.label_power.pack()

        # # Create a button to simulate charging
        # charge_button = ttk.Button(self.frame, text="Charge", command=self.charge_battery, style="Custom.TButton")
        # charge_button.pack()

        #Set the initial color
        self.update_color()

    def charge_battery(self):
        # Simulate charging by increasing the charge level
        self.charge_level += 1
        if self.charge_level > 100:
            self.charge_level = 100

        # Update the battery fill based on the new charge level
        fill_width = (self.charge_level / 100) * 150  # 150 is the maximum width for 100% charge
        self.canvas.coords(self.battery_fill, 25, 25, 25 + fill_width, 75)

        # Update the label to display the new charge level
        self.label_charge.config(text=f"Charge Level: {self.charge_level}%")

        # Update the color based on the charge level
        self.update_color()

    def update_color(self):
        # Determine the color based on the charge level
        if self.charge_level < 20:
            color = "red"
        elif 20 <= self.charge_level <= 70:
            color = "yellow"
        else:
            color = "green"

        # Update the fill color
        self.canvas.itemconfig(self.battery_fill, fill=color)
