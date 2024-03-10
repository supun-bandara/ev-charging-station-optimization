# total backend part
# this code can be used without gui part

# sample_list_from_gui = [id,start_soc, current_soc, end_soc, arrival_time, departure_time, battery_capacity, charging_power, unit_price, grid_price, ev_demand, maximum_grid_demand]

import sys
import os
import pandas as pd
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from charging_station.util.PredictPower import predict_power
from charging_station.util.PredictPrice import predict_price
from backend.convert_array import convert_array

from panda_power.panda import Pandapower

from charging_station.util.processes import remove_EV, process, convert_back
import numpy as np

import random

class chargingStation_backend():
    def __init__(self):
        super(chargingStation_backend, self).__init__()
        self.number_of_chargers = 10
        self.max_charging_power = np.array([100, 100, 100, 100, 25, 25, 25, 25, 25, 25])
        self.max_grid_demand = 360 #previous name = self.maximum_demand # values should be got from outside

    def add_EV(self, charger_id, start_soc,current_soc, end_soc, current_time, departure_time, battery_capacity):
        res_parking_time = chargingStation_backend.time_diff(current_time,departure_time)
        res_charging_demand = battery_capacity * (end_soc - current_soc) / 100
        charging_price = predict_price(self, charger_id, current_time, res_parking_time, res_charging_demand)
        return charging_price

    def next_time(self, current_time, array):
        #print("backend - next_time - current_time: ", current_time, " array: ", array)
        self.chargers = np.zeros(self.number_of_chargers)
        self.res_parking_time = np.zeros(self.number_of_chargers)
        self.res_charging_demand = np.zeros(self.number_of_chargers)
        self.battery_capacity = np.zeros(self.number_of_chargers)
        self.start_soc = np.zeros(self.number_of_chargers)
        self.current_soc= np.zeros(self.number_of_chargers)
        self.end_soc = np.zeros(self.number_of_chargers)
        self.arrival_time =np.array(['00:00','00:00','00:00','00:00','00:00','00:00','00:00','00:00','00:00','00:00'], dtype='str')
        self.departure_time =np.array(['00:00','00:00','00:00','00:00','00:00','00:00','00:00','00:00','00:00','00:00'], dtype='str')
        self.charging_price = np.zeros(self.number_of_chargers)
        self.charging_power = np.zeros(self.number_of_chargers)
        
        convert_array(self, current_time, array)
        
        #pandapower
        grid_power=Pandapower(current_time)  #create pandapower object
        
        grid_power.time_loads_uniform(current_time)
        grid_power.uniform_load()                                       #create all the loads are same
        
        
        grid_power.run_calculation()
        self.max_grid_demand=float(grid_power.maximum_power(78))*1000  #get maximum power of charging station and covert in to kilowatts
        self.max_grid_demand= self.max_grid_demand * random.uniform(0.95, 1)
        
        self.charging_power = predict_power(self, current_time)
        self.total_power = float(np.sum(self.charging_power))
        
        
        
        #grid_power.initialize_network()    #remove unwanted loads and create a pure network
        
        print(self.max_grid_demand)    
        print("total power",self.total_power) 
        grid_power.charging_station_power(78 ,self.total_power,2)      # bus 48(index 78) - charging station / line 183 -line 161
        grid_power.run_calculation()
        
        
        #grid_power.open_network()  #opening the network
        
        process(self)
        remove_EV(self)
        return convert_back(self, current_time)
    
    def _15_min(t):
        t_split = t.split(":")
        hour = int(t_split[0])
        minute = int(t_split[1])
        time_min =hour*60+minute
        _15_min_slots=int(time_min/15)
        
        return _15_min_slots
    
    def time_diff(t1,t2):
               
        t1_split = t1.split(":")
        t2_split = t2.split(":")
        
        # t1_split_hour_and_minutes
        hour = int(t1_split[0])
        minute = int(t1_split[1])
        time1_min =hour*60+minute
        #print("time1",time1_min)
        
        # t2_split_hour_and_minutes
        hour = int(t2_split[0])
        minute = int(t2_split[1])
        time2_min =hour*60+minute
        #print("time2",time2_min)
        
        _15_min_slots=int((time2_min-time1_min)/15)
              
        #print("15 min slots",_15_min_slots)
        return _15_min_slots      


