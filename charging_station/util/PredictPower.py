# charging power prediction for backend

import sys
import os
import pandas as pd
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import numpy as np
from forecasting_models.grid_price_forecaset import grid_price_forecast

def predict_power(self, current_time):
    if self.max_grid_demand >= np.sum(self.max_charging_power * self.chargers): # when the maximum available grid demand is not exceeded
        grid_price = grid_price_forecast(current_time)
        today_max_grid_price = 200
        today_min_grid_price = 10
        max_possible_grid_power = self.max_charging_power * 0.15
        grid_price_component = (grid_price[0] - today_min_grid_price) * max_possible_grid_power / (today_max_grid_price - today_min_grid_price)

        charging_power = self.max_charging_power * 0.8  + grid_price_component
        charging_power = charging_power * self.chargers
        charging_power = self.max_charging_power * self.chargers # np.random.uniform(0.97, 1, 10) * 
        return charging_power
    
    else: # when the maximum available grid demand is exceeded
        dc_count = np.sum(self.chargers[:4])
        if dc_count == 4:
            first_four = np.array([80, 80, 80, 80]) # np.random.randint(15, 17, size=4)
            dc_charging_power = np.concatenate((first_four, np.zeros(6))) * self.chargers
        elif dc_count in [1,2,3]:
            first_four = np.array([100, 100, 100, 100]) # np.random.randint(22, 25, size=4)
            dc_charging_power = np.concatenate((first_four, np.zeros(6))) * self.chargers

        ac_max_grid_demand = self.max_grid_demand - np.sum(dc_charging_power)
        min_charging_rates = np.where(self.res_parking_time[4:] != 0, np.divide(self.res_charging_demand[4:], self.res_parking_time[4:]), 0)
        np.where(self.res_parking_time[4:] != 0, np.divide(self.res_charging_demand[4:], self.res_parking_time[4:]), 0)
        sum_of_min_charging_rates = np.sum(min_charging_rates)
        ac_charging_power = ac_max_grid_demand * min_charging_rates / sum_of_min_charging_rates
        ac_charging_power = np.minimum(ac_charging_power, 25)
        charging_power = np.concatenate((dc_charging_power[:4], ac_charging_power))
        #print("predict_power - charging_power: ", charging_power)
        return charging_power
