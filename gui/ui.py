import sys
import os
import pandas as pd
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import numpy as np

from backend.backend import chargingStation_backend
from gui.configure_model_form import ConfigureModelForm
from gui.ev_forecast_form import EvForecastForm
from gui.battery_ui import BatteryUI
from gui.empty_battery_ui import emptyBatteryUI

chargers=[]
for i in range(10):
    raw_chargers=[]
    for j in range(8):
         raw_chargers.append(int(0))
    chargers.append(raw_chargers)    

class ChargingStation:
    def __init__(self, root, style):
        self.root = root
        self.style = style
        self.empty_slots = []
        self.time = "06:00"
        self.vehicle_batteries = []  
        self.initialize=0
        self.time_diff=15
        self.Grid_price=0
        self.Chargers_prices=0
        self.total_profit=0
        self.total_power=0
        self.max_power=0
        self.ev_forcast=0
        self.empty_slots=[0]*10
        self.index = [0 for i in range(10)]

        self.frame = ttk.Frame(root, padding="5", style="Custom.TFrame")
        self.frame.grid(row=0, column=0, columnspan=10, sticky=tk.W)
        self.font=("Hack Bold", 10)
        
        self.time_label = ttk.Label(self.frame, text=f"Time : {self.time}", font= self.font, style="Custom.TLabel", foreground="red")
        self.time_label.grid(row=0, column=0, ipadx=5)

        self.grid_price_label = ttk.Label(self.frame, text=f"Grid Price: ¢{self.Grid_price}", font= self.font, style="Custom.TLabel", foreground="blue")
        self.grid_price_label.grid(row=0, column=1, ipadx=10)
        
        self.chargers_price_label = ttk.Label(self.frame, text=f"Chargers Income: ${self.Chargers_prices}", font= self.font, style="Custom.TLabel", foreground="blue")
        self.chargers_price_label.grid(row=0, column=2, ipadx=5)
        
        self.profit_label = ttk.Label(self.frame, text=f"Total profit: ${self.total_profit}", font= self.font, style="Custom.TLabel", foreground="blue")
        self.profit_label.grid(row=0, column=3, ipadx=5)

        self.total_power_label = ttk.Label(self.frame, text=f"Total Power: {self.total_power}W", font= self.font, style="Custom.TLabel", foreground="green")
        self.total_power_label.grid(row=0, column=4, ipadx=45)

        self.Grid_power_label = ttk.Label(self.frame, text=f"Grid Max Power: {self.max_power}W", font= self.font, style="Custom.TLabel", foreground="red")
        self.Grid_power_label.grid(row=2, column=4, ipadx=45)
        
        self.ev_demand_label = ttk.Label(self.frame, text=f"EV Demand \nNext Hour: {self.ev_forcast} kW ", font= self.font, style="Custom.TLabel", foreground="black")
        self.ev_demand_label.grid(row=0, column=5, ipadx=25)
        
        self.change_time_button = ttk.Button(self.frame, text="Change Time", command=self.time_pass, style="Custom.TButton")
        self.change_time_button.grid(row=2, column=0, pady=5, sticky=tk.W)

        self.configure_button = ttk.Button(self.frame, text="Configure", command=self.open_configure_form, style="Custom.TButton")
        self.configure_button.grid(row=2, column=2, sticky=tk.W, ipadx=10)
        
        self.configure_button = ttk.Button(self.frame, text="EV Forecast", command=self.open_EV_form, style="Custom.TButton")
        self.configure_button.grid(row=2, column=5, sticky=tk.W)
     
        self.add_button = ttk.Button(self.frame, text="Add Vehicle", command=self.open_form, style="Custom.TButton")
        self.add_button.grid(row=2, column=3, sticky=tk.W)

        self.run_every_minute_button = ttk.Button(self.frame, text="Run Every Minute", command=self.run_every_minute, style="Custom.TButton")
        self.run_every_minute_button.grid(row=2, column=1, pady=5, sticky=tk.W)

        for i in range(10):
            self.create_empty_slot(i) 
               
        self.initialize_chargers()

    def run_every_minute(self):
        self.time_pass()
        self.root.after(60000, self.run_every_minute)
            
    def empty_slots_create(self,charger_id):
        self.index[charger_id]=0
        self.create_empty_slot(charger_id)  
        
    def initialize_chargers(self):
        self.initialize=1
        return self.initialize
              
    def create_empty_slot(self,charger_id):
        empty_slot = self.create_empty_battery_ui(charger_id)
        self.empty_slots[charger_id]=empty_slot

    def add_vehicle_battery(self, vehicle_data):
        charger_id=vehicle_data[0]
        if charger_id<5:
            BatteryUI(self.root, self.style, charger_id, 3,*vehicle_data)
        elif charger_id>=5:   
            rest_data=vehicle_data[1:10]
            BatteryUI(self.root, self.style, charger_id, 4,charger_id-5,*rest_data)
        
    def add_empty_charger(self, vehicle_data):
        charger_id=vehicle_data[0]
        if charger_id<5:
            empty_battery_ui=emptyBatteryUI(self.root, self.style, charger_id, 3,*vehicle_data)
            return empty_battery_ui
        elif charger_id>=5:   
            rest_data=vehicle_data[1:]
            empty_battery_ui=emptyBatteryUI(self.root, self.style, charger_id, 4,charger_id-5,*rest_data) 
            return empty_battery_ui
                          
    def create_empty_battery_ui(self, charger_id,):
        if charger_id<5:
            empty_battery_ui = emptyBatteryUI(self.root, self.style, charger_id, 3,charger_id, 0, 0, 0,0, 0,0,0)
            return empty_battery_ui
        
        elif charger_id>=5:   
            empty_battery_ui = emptyBatteryUI(self.root, self.style, charger_id, 4,charger_id-5, 0, 0, 0,0, 0,0,0)
            return empty_battery_ui
  
    def open_form(self):
        form_window = ChargingStationForm(self.root, self)

    def time_pass(self):
        self.change_time()
        global chargers
        backend_receice_array = chargingStation_backend.next_time(chargingStation_backend(),self.time,chargers)
        chargers = backend_receice_array[:len(backend_receice_array)-2]
        self.Grid_price_forecast = backend_receice_array[len(backend_receice_array)-2]
        self.ev_forecast = backend_receice_array[len(backend_receice_array)-1]

        self.Grid_price = self.Grid_price_forecast[0]  

        self.grid_price_label.config(text=f"Grid Price: ¢{self.Grid_price}")

        self.next1_hour = self.ev_forecast[0]
        self.ev_demand_label.config(text=f"EV Demand \nNext Hour: {self.next1_hour} kW ")

        self.total_power = 0
        for i in range(len(chargers)): 
            if chargers[i][2] != 0:
                self.total_power += int(chargers[i][len(chargers[i])-2])

        self.total_power_label.config(text=f"Total Power: {self.total_power} kW ")

        self.Chargers_prices = 0
        for i in range(len(chargers)): 
            if chargers[i][2] != 0:
                self.Chargers_prices += int(chargers[i][len(chargers[i])-1])
        self.chargers_price_label.config(text=f"Chargers Income: ${self.Chargers_prices}")  

        self.profit_label.config(text=f"Total Profit: ${self.max_power}") 
        self.Grid_power_label.config(text=f"Grid Max Power: ${self.max_power}")         

        for i in range(len(chargers)): 
            if chargers[i][2] != 0:
                self.add_vehicle_battery(chargers[i])
            else:    
                self.empty_slots_create(chargers[i][0])

    def change_time(self,):
        # Extract only the numeric part of the time string
        current_time = self.time_label["text"]
        numeric_parts = current_time.split(":")
        #print(numeric_parts)
        # Extract hour and handle the case where there is no minute part
        hour = int(current_time.split(":")[1])
        minute = int(current_time.split(":")[2])
        #print(hour)
        #print(minute)

        # Increment the time by 15 minutes
        minute += 15

        # Adjust the hour and minute if necessary
        if minute >= 60:
            minute %= 60
            hour = (hour + 1) % 24

        # Format the new time and update the label
        new_time = f"Current time : {hour:02d}:{minute:02d}"
        charging_station.time=f"{hour:02d}:{minute:02d}"
        self.time_label.config(text=new_time)

    def open_configure_form(self):
        # Open the ConfigureModelForm window
        configure_form_window = ConfigureModelForm(self.root)
        
    def open_EV_form(self):
        # Open the ConfigureModelForm window
        configure_form_window = EvForecastForm(self.root, self) 
class ChargingStationForm(tk.Toplevel):
    def __init__(self, parent, charging_station):
        super().__init__(parent)
        
        self.configure(bg='#1fd655')
        style.configure("bag.TLabel", background="#1fd655")
        style.configure("bag.TCheckbutton", background="#1fd655",padding=(20,10))
        
        self.title("Add Vehicle")
        self.geometry("500x400")
        self.charging_station = charging_station
        self.vehicle_id=0
        self.frame = ttk.Frame(root, padding="10", style="Custom.TFrame")
        self.frame.grid(row=0, column=0, columnspan=10)
        font=("Hack Regular", 10)

       # Charger Type
        self.charger_type_label = ttk.Label(self, text="Charger Type:", style="bag.TLabel", font=font)
        self.charger_type_label.grid(row=0, column=0, pady=10, padx=25)
        self.charger_type = ttk.Combobox(self, values=("AC", "DC"), style="bag.TCombobox")
        self.charger_type.grid(row=0, column=1, pady=10, padx=25)
        self.charger_type.current(0)  # Default selection is "AC"
        '''
        # Create labels and entry widgets for user input
        self.Charger_id_label=ttk.Label(self, text="Charger id:",style="bag.TLabel",font=font)
        self.Charger_id_label.grid(row=2, column=0,pady=10, padx=25)
        self.Charger_id_ = tk.Spinbox(self, from_=0, to=9)
        self.Charger_id_.grid(row=2, column=1,pady=10, padx=25)
        '''
        self.Current_SOC_label=ttk.Label(self, text="Current SOC :",style="bag.TLabel",font=font)
        self.Current_SOC_label.grid(row=3, column=0,pady=10, padx=25)
        self.soc_entry = tk.Spinbox(self, from_=0, to=100)
        self.soc_entry.grid(row=3, column=1,pady=10, padx=25)
        
        self.Require_SOC_label=ttk.Label(self, text="Require SOC :",style="bag.TLabel",font=font)
        self.Require_SOC_label.grid(row=4, column=0,pady=10, padx=25)
        self.rsoc_entry = tk.Spinbox(self, from_=int(self.soc_entry.get()), to=100)
        self.rsoc_entry.grid(row=4, column=1,pady=10, padx=25)

        self.Departure_Time_label=ttk.Label(self, text="Departure Time (hh:mm) :",style="bag.TLabel",font=font)
        self.Departure_Time_label.grid(row=5, column=0,pady=10, padx=25)
        self.time_entry = ttk.Entry(self, width=20)
        self.time_entry.grid(row=5, column=1,pady=10, padx=25)

        self.Battery_Capacity_label=ttk.Label(self, text="Battery Capacity :",style="bag.TLabel",font=font)
        self.Battery_Capacity_label.grid(row=6, column=0,pady=10, padx=25)
        self.capacity_entry = ttk.Entry(self, width=20)
        self.capacity_entry.grid(row=6, column=1,pady=10, padx=25)

        self.error_label = ttk.Label(self, text="", foreground="red",style="bag.TLabel",font=font)
        self.error_label.grid(row=7, column=1,pady=10, padx=25,sticky=tk.W)

        # Create a button to submit the form
        self.Battery_Capacity_button=ttk.Button(self, text="Add Vehicle", command=self.add_vehicle,style="Custom.TButton")
        self.Battery_Capacity_button.grid(row=7, column=0,pady=10, padx=50)

        # Create a button to choose sample data
        self.sample_data_button = ttk.Button(self, text="Choose Sample Data", command=self.choose_sample_data)
        self.sample_data_button.grid(row=8, column=0, columnspan=2, pady=10)

    def choose_sample_data(self):
        # Here you can implement logic to choose which sample data to fill in the form
        # For demonstration purposes, let's say we're choosing the first sample data
        self.charger_type.current(0)  # Charger Type: AC
        self.soc_entry.delete(0, tk.END)
        self.soc_entry.insert(0, "10")  # Current SOC: 10
        self.rsoc_entry.delete(0, tk.END)
        self.rsoc_entry.insert(0, "90")  # Require SOC: 90
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, "12:00")  # Departure Time: 12:00
        self.capacity_entry.delete(0, tk.END)
        self.capacity_entry.insert(0, "100")  # Battery Capacity: 100
        
    def add_vehicle(self):
        try:
            # Retrieve user input and create a new ChargingStation instance
            #charger_id = int(self.Charger_id_.get())
            current_soc = float(self.soc_entry.get())
            required_soc=float(self.rsoc_entry.get())
            departure_time = self.time_entry.get()  # Keep it as a string for now
            try:
                battery_capacity = int(self.capacity_entry.get())
            except ValueError:
                self.error_label.config(text="Battery capacity must be a number")
                return

            # Validate SOC value           
            if not 0 <= current_soc <= 100:
                raise ValueError("SOC must be between 0 and 100")

            # Validate departure time format
            # You may want to add more sophisticated time validation
            if len(departure_time) != 5 or not departure_time[2] == ":":
                raise ValueError("Invalid departure time format. Use hh:mm")
            
            arrival_time=charging_station.time

            charger_type = self.charger_type.get()
            
            # Assign charger based on charger type and availability
            if charger_type == "DC":
                for idx in range(4):
                    if self.charging_station.index[idx] == 0:  # Charger is available
                        charger_id = idx
                        self.charging_station.index[idx] = 1  # Mark charger as occupied
                        break
                else:
                    raise ValueError("No available DC charger found")
            else:  # AC charger
                for idx in range(4, 10):
                    if self.charging_station.index[idx] == 0:  # Charger is available
                        charger_id = idx
                        self.charging_station.index[idx] = 1  # Mark charger as occupied
                        break
                else:
                    raise ValueError("No available AC charger found")

            vehicle_data = [charger_id,current_soc,required_soc,arrival_time,departure_time,battery_capacity ]
            charging_price=chargingStation_backend.add_EV(chargingStation_backend(),*vehicle_data)
            
            charging_power=0
            vehicle_data.append(charging_power)
            vehicle_data.append(charging_price)           
            #print(vehicle_data)
            
            chargers[charger_id]=vehicle_data
            #print(chargers)

            # Add the vehicle's battery to the charging station
            self.charging_station.add_vehicle_battery(vehicle_data)
         
            # Close the form window
            self.destroy()

        except ValueError as e:
            # Handle the validation error
            self.error_label.config(text=str(e))


if __name__ == "__main__":
    root = tk.Tk()

    root.title("Charging station optimization software using reinforcement learning")
    # Create a custom theme
    root.tk_setPalette(background='#ececec', foreground='#000000', activeBackground='#b5e2ff', activeForeground='#000000')

    style = ttk.Style()
    style.configure("Custom.TFrame", background="#CBC3E3")
    style.configure("Custom.TLabel", background="#CBC3E3")
    style.configure("Custom.TButton", background="#b5e2ff",font=("Hack Regular", 10))

    # Set the window size
    window_width = 1500
    window_height = 700
    root.geometry(f"{window_width}x{window_height}")

    # # Create 10 BatteryUI instances arranged in 2 rows with 5 columns
    # prices = [50, 60, 70, 80, 90, 100, 110, 120, 130, 140]
    # powers = [300, 350, 400, 450, 500, 550, 600, 650, 700, 750]
    # charging_price = [200, 49, 788, 888, 234, 456, 764, 678, 786, 898]
    # charging_station_power = sum(powers)
    charging_station = ChargingStation(root, style)
    
    root.configure(background='#CBC3E3')
    
    root.mainloop()