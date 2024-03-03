# charging power prediction for backend

import sys
import os
import pandas as pd
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import numpy as np
from forecasting_models.grid_price_forecaset import grid_price_forecast

def predict_power(self, current_time):
    if self.max_grid_demand >= self.max_charging_power * np.sum(self.chargers == 1):
        
        grid_price = grid_price_forecast(current_time)
        today_max_grid_price = 200
        today_min_grid_price = 10
        max_possible_grid_power = self.max_charging_power * 0.15
        grid_price_component = (grid_price[0] - today_min_grid_price) * max_possible_grid_power / (today_max_grid_price - today_min_grid_price)

        charging_power = self.max_charging_power * 0.8  + grid_price_component
        charging_power = np.full(self.number_of_chargers, charging_power) * self.chargers
        #print("predict_power - charging_power: ", charging_power)
        return charging_power
        # return np.random.uniform(0.85, 1, self.number_of_chargers) * self.max_charging_power * self.chargers
    else:
        products = self.res_parking_time * self.res_charging_demand
        #print("predict_power - products", products)
        sum_of_products = np.sum(products)
        #print("predict_power - sum_of_products", sum_of_products)
        charging_power = self.max_grid_demand * products / sum_of_products
        #print("predict_power - charging_power: ", charging_power)
        return charging_power
