# ev forecasting model
# give inputs in hours

import pandas as pd
import pickle
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt

def ev_demand_forecast(ref):
    current_timestamp = pd.to_datetime("2023-09-02 " + ref)
    future_df = pd.DataFrame(columns=['year', 'month', 'day', 'hour'])
    model_filename = 'forecasting_models/trained_model_energy.pkl'
    loaded_model = pickle.load(open(model_filename, 'rb'))
    
    for i in range(12):
        future_timestamp = current_timestamp + timedelta(hours=i)
        year = future_timestamp.year
        month = future_timestamp.month
        day = future_timestamp.day
        hour = future_timestamp.hour
        new_row_df = pd.DataFrame({'year': [year], 'month': [month], 'day': [day], 'hour': [hour]})
        future_df = pd.concat([future_df, new_row_df], ignore_index=True)

    future_df_int = future_df.astype(int)
    predicted_charging_power = loaded_model.predict(future_df_int)
    predicted_charging_power = predicted_charging_power*9
    return  np.round(predicted_charging_power, decimals=2)

def plot():
    x_values = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
    y_values = ev_demand_forecast('00:00')
    plt.plot(x_values, y_values)
    plt.ylabel('EV demand')
    plt.xlabel('date')
    plt.title("EV demand vs Date")
    plt.xticks(rotation='vertical')
    plt.show()
    return

#plot()
#print(ev_demand_forecast('00:00'))