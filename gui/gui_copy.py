import sys
import os
import pandas as pd
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import numpy as np

from backend.backend import chargingStation_backend
#initialize the chargers

from PIL import Image, ImageTk

chargers=[]
for i in range(10):
    raw_chargers=[]
    for j in range(8):
         raw_chargers.append(int(0))
    chargers.append(raw_chargers)    

#print("init charger:",chargers)
class ConfigureModelForm(tk.Toplevel):
    def __init__(self, parent): 
        super().__init__(parent)
        self.title("Configure Model")
        self.geometry("200x150")

        # Create buttons for model configuration
        ttk.Button(self, text="Train Model", command=self.train_model).pack(pady=5)
        ttk.Button(self, text="Test Model", command=self.test_model).pack(pady=5)
        ttk.Button(self, text="Save Model", command=self.save_model).pack(pady=5)
        ttk.Button(self, text="Show Plots", command=self.show_plots).pack(pady=5)

    def train_model(self):
        # Implement the logic for training the model
        messagebox.showinfo("Train Model", "Model training functionality to be implemented.")

    def test_model(self):
        # Implement the logic for testing the model
        messagebox.showinfo("Test Model", "Model testing functionality to be implemented.")

    def save_model(self):
        # Implement the logic for saving the model
        messagebox.showinfo("Save Model", "Model saving functionality to be implemented.")

    def show_plots(self):
        # Implement the logic for showing plots
        messagebox.showinfo("Show Plots", "Plot display functionality to be implemented.")

class EvforcastForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("EV forcast ")
        self.geometry("200x180")
        
        forcast_detail=charging_station.Grid_price_forecast
        
        for i in range(1,7):
            ttk.Label(self, text=f"Next {i} hour: {forcast_detail[i-1]}kW").pack(pady=5)

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
        
        
       # DC Charger
        self.DC_label =ttk.Label(self, text="DC Charger:",style="bag.TLabel",font=font)
        self.DC_label.grid(row=0, column=0,pady=10, padx=25)
        self.DC_charger = ttk.Checkbutton(self,onvalue=True,style="bag.TCheckbutton")
        self.DC_charger.grid(row=1, column=0, padx=25,ipadx=10)
        
        # AC Charger
        self.AC_label=ttk.Label(self, text="AC Charger:",style="bag.TLabel",font=font)
        self.AC_label.grid(row=0, column=1,pady=10, padx=10)
        self.AC_charger = ttk.Checkbutton(self,onvalue=True,style="bag.TCheckbutton")
        self.AC_charger.grid(row=1, column=1, padx=25)
        
        # Create labels and entry widgets for user input
        self.Charger_id_label=ttk.Label(self, text="Charger id:",style="bag.TLabel",font=font)
        self.Charger_id_label.grid(row=2, column=0,pady=10, padx=25)
        self.Charger_id_ = tk.Spinbox(self, from_=0, to=9)
        self.Charger_id_.grid(row=2, column=1,pady=10, padx=25)
        
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
        
        
    def add_vehicle(self):
        
        try:
            # Retrieve user input and create a new ChargingStation instance
            charger_id = int(self.Charger_id_.get())
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


class ChargingStation:
    def __init__(self, root):
        self.root = root
        self.empty_slots = []
        self.time = "06:00"
        self.vehicle_batteries = []  # Store added vehicle batteries
        # Create a frame for the charging station price and power
        self.initialize=0
        #print(self.initialize)
        self.time_diff=15
        self.Grid_price=0
        self.Chargers_prices=0
        self.total_profit=0
        self.total_power=0
        self.max_power=0
        
        self.ev_forcast=0
        
        self.empty_slots=[0]*10
        
        self.frame = ttk.Frame(root, padding="10", style="Custom.TFrame")
        self.frame.grid(row=0, column=0, columnspan=10, sticky=tk.W)
        
        
        self.font=("Hack Bold", 13)
        
        # Create a label to display the charging station time
        self.time_label = ttk.Label(self.frame, text=f"Current time : {self.time}", font= self.font,
                                    style="Custom.TLabel", foreground="red")
        self.time_label.grid(row=0, column=0, ipadx=10)

        # Create a label to display the grid price
        self.grid_price_label = ttk.Label(self.frame, text=f"Grid Unit Price: ¢{self.Grid_price}", font= self.font,
                                     style="Custom.TLabel", foreground="blue")
        self.grid_price_label.grid(row=0, column=1, ipadx=20)
        
        # Create a label to display the charging station price
        self.chargers_price_label = ttk.Label(self.frame, text=f"Chargers Income: ${self.Chargers_prices}", font= self.font,
                                     style="Custom.TLabel", foreground="blue")
        self.chargers_price_label.grid(row=0, column=2, ipadx=10)
        
        
        # Create a label to display the charging station price
        self.profit_label = ttk.Label(self.frame, text=f"Total profit: ${self.total_profit}", font= self.font,
                                     style="Custom.TLabel", foreground="blue")
        self.profit_label.grid(row=0, column=3, ipadx=10)

        # Create a label to display the charging station power
        self.total_power_label = ttk.Label(self.frame, text=f"Total Power: {self.total_power}W", font= self.font,
                                     style="Custom.TLabel", foreground="green")
        self.total_power_label.grid(row=0, column=4, ipadx=85)

        # Create a label to display the charging station power
        self.Grid_power_label = ttk.Label(self.frame, text=f"Grid Max Power: {self.max_power}W", font= self.font,
                                     style="Custom.TLabel", foreground="red")
        self.Grid_power_label.grid(row=2, column=4, ipadx=85)
        
        # Create a label to display the charging station power
        self.ev_demand_label = ttk.Label(self.frame, text=f"EV forecast Damand \nnext 1 hour:{self.ev_forcast} ", font= self.font,
                                     style="Custom.TLabel", foreground="black")
        self.ev_demand_label.grid(row=0, column=5, ipadx=50)
        
        
        
        # Create a button to change the current time
        self.change_time_button = ttk.Button(self.frame, text="Change Time", command=self.time_pass,
                                             style="Custom.TButton")
        self.change_time_button.grid(row=2, column=0,pady=20,sticky=tk.W)

        # Create a button to for configure the charging station
        self.configure_button = ttk.Button(self.frame, text="Configure", compound=tk.LEFT, command=self.open_configure_form,style="Custom.TButton")
        self.configure_button.grid(row=2, column=2, sticky=tk.W,ipadx=10)
        
        
        # Create a button to for open EV forecasting model
        self.configure_button = ttk.Button(self.frame, text="EV forecast", command=self.open_EV_form,style="Custom.TButton")
        self.configure_button.grid(row=2, column=5, sticky=tk.W)
     
        # Create a button to add the vehicle
        self.add_button = ttk.Button(self.frame, text="Add Vehicle", command=self.open_form,style="Custom.TButton")
        self.add_button.grid(row=3, column=0,sticky=tk.W)

        #initialize_chargers
        for i in range(10):
            self.create_empty_slot(i) 
               
        self.initialize_chargers()
            
    def empty_slots_create(self,charger_id):
        
        
        self.create_empty_slot(charger_id)  
        
               
    def initialize_chargers(self):
        self.initialize=1
        #print(self.initialize)
        return self.initialize
              
    def create_empty_slot(self,charger_id):
        # Create an empty slot (rectangle) and store its reference
        
        
        empty_slot = self.create_empty_battery_ui(charger_id)
        self.empty_slots[charger_id]=empty_slot


    def add_vehicle_battery(self, vehicle_data):
        # Check if there are empty slots available
            # Get the reference of the first empty slot
            charger_id=vehicle_data[0]
            #print(charger_id)
            if charger_id<5:
                BatteryUI(self.root, charger_id, 3,*vehicle_data)
            elif charger_id>=5:   
                rest_data=vehicle_data[1:10]
                BatteryUI(self.root, charger_id, 4,charger_id-5,*rest_data)
        
    def add_empty_charger(self, vehicle_data):
        # Check if there are empty slots available
            # Get the reference of the first empty slot
            charger_id=vehicle_data[0]
            #print(charger_id)
            #print(charger_id)                       
            if charger_id<5:
                empty_battery_ui=emptyBatteryUI(self.root, charger_id, 3,*vehicle_data)
                return empty_battery_ui
            elif charger_id>=5:   
                rest_data=vehicle_data[1:]
                empty_battery_ui=emptyBatteryUI(self.root, charger_id, 4,charger_id-5,*rest_data) 
                return empty_battery_ui
                          
    def create_empty_battery_ui(self, charger_id,):
        # Create an empty BatteryUI instance with initial data 
                                       
        if charger_id<5:
            empty_battery_ui = emptyBatteryUI(self.root, charger_id, 3,charger_id, 0, 0, 0,0, 0,0,0)
            return empty_battery_ui
        
        elif charger_id>=5:   
            empty_battery_ui = emptyBatteryUI(self.root, charger_id, 4,charger_id-5, 0, 0, 0,0, 0,0,0)
            return empty_battery_ui
  
    def open_form(self):
        # Open the ChargingStationForm window
        form_window = ChargingStationForm(self.root, self)

    def time_pass(self):
        self.change_time()
        #print("current_time",self.time)
        global chargers
        #print("send array")
        #for i in  range(10):
           #print(i,chargers[i]) 
           
        ####################################
        backend_receice_array = chargingStation_backend.next_time(chargingStation_backend(),self.time,chargers)
        ###################################
        chargers=backend_receice_array[:len(backend_receice_array)-2]  #choose the charger details
        ####################################
        self.Grid_price_forecast=backend_receice_array[len(backend_receice_array)-2] #choose the grid price forecasting details
        #print("Grid_price_forecast details",self.Grid_price_forecast)
        ####################################
        self.ev_forecast= backend_receice_array[len(backend_receice_array)-1]  #choose the ev forecasting details
        #print("EV forcasting details",self.ev_forecast)
        
        
        
        ###############################
        #update the grid price 
        self.Grid_price=self.Grid_price_forecast[0]  #select the first one  
  
        self.grid_price_label.config(text=f"Grid Unit Price:¢{self.Grid_price}")
                               
        
        ################################
        # update the EV forecasting next 1 hour
        self.next1_hour=self.ev_forecast[0]
        self.ev_demand_label.config(text=f"EV forecast Damand \nnext 1 hour:{self.next1_hour}kW ")
          
          
        ################################
        #update the total power
        self.total_power=0
        for i in range(len(chargers)): 
            # [id, current_soc, end_soc, arrival_time, departure_time, battery_capacity, charging_price, charging_power,grid_price,ev_demand]            
            #ChargingStation.add_vehicle_battery(self,chargers[i])
            if chargers[i][2]!=0:
               self.total_power+=int(chargers[i][len(chargers[i])-2])
        
        
        self.total_power_label.config(text=f"Total Power :{self.total_power}kW ")

        ########################
        #update the total prices
        self.Chargers_prices=0
        for i in range(len(chargers)): 
            # [id, current_soc, end_soc, arrival_time, departure_time, battery_capacity,  charging_power,charging_price,,grid_price,ev_demand]            
            #ChargingStation.add_vehicle_battery(self,chargers[i])
            if chargers[i][2]!=0:
               self.Chargers_prices+=int(chargers[i][len(chargers[i])-1])
        
        
        self.chargers_price_label.config(text=f"Chargers Income :${self.Chargers_prices}")  

            
        ######################################
        #update the profit
        
        self.profit_label.config(text=f"Total profit :${self.max_power}") 
         
         
        ######################################
        #update the maximim power        
        # self.total_profit=backend_receice_array[]
        self.Grid_power_label.config(text=f"Grid Max Power :${self.max_power}")         
        #print("receive array")
        for i in range(len(chargers)): 
            #print(chargers[i])
            #ChargingStation.add_vehicle_battery(self,chargers[i])
            if chargers[i][2]!=0:
                #print() #choose the vehicle data
                self.add_vehicle_battery(chargers[i])
            else:    
                self.empty_slots_create(chargers[i][0])
                
    def remove_battery(self,charger_id):
        emptyBatteryUI(self.root, charger_id, 3,charger_id, 0, 0, 0,0, 0,0,0)
    
        
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
        configure_form_window = EvforcastForm(self.root)    



class BatteryUI:
    
    def __init__(self, root, charger_id, row, col,current_soc,required_soc,arrival_time,departure_time,battery_capacity,charging_power,charging_price):
        self.root = root

        # Create a frame for each battery
        style.configure("battery.TFrame", background="#CBC3E3")
        
        self.frame = ttk.Frame(root, padding="10", style="battery.TFrame")
        self.frame.grid(row=row, column=col, padx=5, pady=5)
        
        #battery id
        self.charger_id=charger_id
               
        # Set initial charge level (between 0 and 100)//map to 100 with filling the rectangle
        self.charge_level = (current_soc / 100) * 150

        #required SOC
        self.required_soc = required_soc
        
        #arrival time
        self.arrival_time = arrival_time
        
        #depature time
        self. departure_time = departure_time
        
        # Set battery capacity
        self.battery_capacity = battery_capacity
        
        # Set charging power 
        self.chariging_power = charging_power

        # Set charging price
        self.charging_price = charging_price

        # Change the background color of the root window
        self.root.configure(background='#CBC3E3')

        font=("Hack Regular", 10)
        # Draw the battery outline
        self.canvas = tk.Canvas(self.frame, width=200, height=100, bg="#CBC3E3", highlightthickness=2)
        self.canvas.pack()
        
        # Draw the battery border
        self.canvas.create_rectangle(20, 20, 180, 80, outline="white", width=5)
        self.canvas.create_rectangle(180, 35, 195, 65, outline="white", width=5)

        # Draw the battery fill based on the initial charge level
        self.battery_fill = self.canvas.create_rectangle(25, 25, 25 + self.charge_level, 75, outline="", fill="green")

        #Battery id
        self.label_charger_id = ttk.Label(self.frame, text=f"Charger id: {self.charger_id}", background="#CBC3E3",
                                      foreground="black", font=font)
        self.label_charger_id.pack()
        
        # Create a label to display the charge level
        self.label_charge = ttk.Label(self.frame, text=f"Charge Level: {current_soc}%", background="#CBC3E3",
                                      foreground="black", font=font)
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

class emptyBatteryUI:
    def __init__(self, root, charger_id, row, col,current_soc,required_soc,arrival_time,departure_time,battery_capacity,charging_power,charging_price):
        self.root = root

        # Create a frame for each battery
        style.configure("battery.TFrame", background="#CBC3E3")
        
        self.frame = ttk.Frame(root, padding="10", style="battery.TFrame")
        self.frame.grid(row=row, column=col, padx=5, pady=5)
        
        #battery id
        self.charger_id=charger_id        

               # Change the background color of the root window
        self.root.configure(background='#CBC3E3')

        self.font=("Hack Regular", 10,)
        
        # Draw the battery outline
        self.canvas = tk.Canvas(self.frame, width=200, height=200, bg="#CBC3E3", highlightthickness=2)
        
        if self.charger_id<=3:            
            emptyBatteryUI.dc_charger_icon(self)
        
        elif self.charger_id>3:
            emptyBatteryUI.ac_charger_icon(self)
       
    def dc_charger_icon(self):

            #print("succes")
                
            self.charger_icon_path = "gui\icons\DC-charger.png"  # Replace with the actual path to your charger icon
            self.charger_icon = tk.PhotoImage(file=self.charger_icon_path)
            
            x_center = self.canvas.winfo_reqwidth() // 2
            y_center = self.canvas.winfo_reqheight() // 2
                       
            self.canvas.create_image(x_center, y_center, image=self.charger_icon)
            self.canvas.pack()
            
            self.label_charge = ttk.Label(self.frame, text=f"        ", background="#CBC3E3",
                                        foreground="black", font=self.font)
            self.label_charge.pack()
            self.label_charge = ttk.Label(self.frame, text=f"DC Charger: {self.charger_id}", background="#CBC3E3",
                                        foreground="black", font=self.font)
            self.label_charge.pack()
                      
    def ac_charger_icon(self):
         
            self.charger_icon_path = "gui\icons\AC-chargers.png"  # Replace with the actual path to your charger icon
            self.charger_icon = tk.PhotoImage(file=self.charger_icon_path)
            
            x_center = self.canvas.winfo_reqwidth() // 2
            y_center = self.canvas.winfo_reqheight() // 2
            self.canvas.create_image(x_center, y_center, image=self.charger_icon) 
            self.canvas.pack()
            
            self.label_charge = ttk.Label(self.frame, text=f"        ", background="#CBC3E3",
                                        foreground="black", font=self.font)
            self.label_charge.pack()
            self.label_charge = ttk.Label(self.frame, text=f"AC Charger: {self.charger_id}", background="#CBC3E3",
                                        foreground="black", font=self.font)
            self.label_charge.pack()        

    
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
    charging_station = ChargingStation(root)
    
    root.configure(background='#CBC3E3')
    
    root.mainloop()
    
