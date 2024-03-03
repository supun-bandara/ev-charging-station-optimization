import sys
import os
import pandas as pd
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import numpy as np
from forecasting_models.grid_price_forecaset import grid_price_forecast
from forecasting_models.EV_demand_forecast import ev_demand_forecast

def remove_EV(self):
    for i in range(len(self.chargers)):
        if self.res_parking_time[i] == 0 and (self.chargers[i] != 0 or self.res_charging_demand[i] != 0): # departure time is reached
            self.res_charging_demand[i] = 0
            self.battery_capacity[i] = 0
            self.chargers[i] = 0
            self.current_soc[i] = 0
            self.end_soc[i] = 0
            self.arrival_time[i] = '00:00'
            self.departure_time[i] = '00:00'
            self.charging_price[i] = 0
            self.charging_power[i] = 0
        if self.res_charging_demand[i] == 0 and (self.chargers[i] != 0 or self.res_parking_time[i] != 0): # charging demand is met
            self.res_parking_time[i] = 0
            self.battery_capacity[i] = 0
            self.chargers[i] = 0
            self.current_soc[i] = 0
            self.end_soc[i] = 0
            self.arrival_time[i] = '00:00'
            self.departure_time[i] = '00:00'
            self.charging_price[i] = 0
            self.charging_power[i] = 0
    return

'''def process(self):
    #print("process - res_parking_time: ", self.res_parking_time)
    self.res_parking_time = self.res_parking_time - 1
    #print("process - res_parking_time: ", self.res_parking_time)
    #print("process - res_charging_demand: ", self.res_charging_demand)
    self.res_charging_demand = self.res_charging_demand - self.charging_power
    #print("process - res_charging_demand: ", self.res_charging_demand)
    #print("process - current_soc: ", self.current_soc)
    np.seterr(divide='ignore', invalid='ignore')
    self.current_soc = np.where(self.battery_capacity != 0, ( self.end_soc - (np.divide(self.res_charging_demand, self.battery_capacity))*100 ), 0)
    np.seterr(divide='warn', invalid='warn')
    #print("process - current_soc: ", self.current_soc)
    return'''

def process(self):
    self.res_parking_time = self.res_parking_time - 1
    self.res_charging_demand = np.clip(self.res_charging_demand - self.charging_power, 0, None)
    np.seterr(divide='ignore', invalid='ignore')
    self.current_soc = np.where(self.battery_capacity != 0, (self.end_soc - (np.divide(self.res_charging_demand, self.battery_capacity))*100), 0)
    self.current_soc = np.clip(self.current_soc, 0, 100)
    np.seterr(divide='warn', invalid='warn')
    return

def convert_back(self, current_time):
    lst = []
    for i in range(len(self.chargers)):
        lst.append([i, round(self.current_soc[i], 3), self.end_soc[i], self.arrival_time[i], self.departure_time[i], self.battery_capacity[i], round(self.charging_power[i], 3), self.charging_price[i]])
    
    # Round values in ev_demand_forecast to 3 decimal places
    grid_price_forecast_result = grid_price_forecast(current_time).tolist()  #convert numpy array to normal list
    grid_price_forecast_rounded = [round(value, 3) for value in grid_price_forecast_result]
    lst.append(grid_price_forecast_rounded)

    # Round values in ev_demand_forecast to 3 decimal places
    ev_demand_forecast_result = ev_demand_forecast(current_time).tolist()   #convert numpy array to normal list
    ev_demand_forecast_rounded = [round(value, 3) for value in ev_demand_forecast_result]
    lst.append(ev_demand_forecast_rounded)

    #print("convert_back - lst: ", lst)
    return lst

# [id,start_soc, current_soc, end_soc, arrival_time, departure_time, battery_capacity, charging_power, unit_price, grid_price, ev_demand, maximum_grid_demand]
