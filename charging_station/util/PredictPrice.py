# charging price prediction for backend

import sys
import os
import pandas as pd
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import numpy as np
from forecasting_models.grid_price_forecaset import grid_price_forecast
from forecasting_models.EV_demand_forecast import ev_demand_forecast

def predict_price(self, charger_id, current_time, res_parking_time, res_charging_demand):
    #print("predict_price - charger_id: ", charger_id, " current_time: ", current_time, " res_charging_demand: ", res_charging_demand, " res_parking_time: ", res_parking_time)
    grid_price = grid_price_forecast(current_time)
    print("predict_price - grid_price: ", grid_price)
    ev_demand = ev_demand_forecast(current_time)
    print("predict_price - ev_demand: ", ev_demand)

    service_fee = 5

    if charger_id in [0,1,2,3]:
        installation_cost = 20
    else:
        installation_cost = 2

    ev_constant = (res_charging_demand/res_parking_time) # normalize this
    grid_price_constant = grid_price[0] * 1.1
    grid_price_forecast_constant = sum(grid_price)*0.1/13
    ev_demand_forecast_constant = sum(ev_demand[:6])*0.1/6
    installation_cost = installation_cost

    charging_price = grid_price_constant + grid_price_forecast_constant + ev_demand_forecast_constant + ev_constant + installation_cost + service_fee # normalize this and add grid price forecast
    print("predict_price - charging_price: ", charging_price, "grid_price_constant: ", grid_price_constant, "grid_price_forecast_constant: ", grid_price_forecast_constant, "ev_demand_forecast_constant: ", ev_demand_forecast_constant, "ev_constant: ", ev_constant, "installation_cost: ", installation_cost, "service_fee: ", service_fee)
    charging_price = charging_price/100
    return round((charging_price), 3)
