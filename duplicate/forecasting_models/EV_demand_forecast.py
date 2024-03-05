# ev forecasting model
# give inputs in hours

import pandas as pd
import pickle
from datetime import datetime, timedelta
import numpy as np

def ev_demand_forecast(ref):
    current_timestamp = pd.to_datetime("2024-02-02 " + ref)
    future_df = pd.DataFrame(columns=['year', 'month', 'day', 'hour'])
    model_filename = 'forecasting_models/trained_model_energy.pkl'
    loaded_model = pickle.load(open(model_filename, 'rb'))
    
    for i in range(6):
        future_timestamp = current_timestamp + timedelta(hours=i)
        year = future_timestamp.year
        month = future_timestamp.month
        day = future_timestamp.day
        hour = future_timestamp.hour
        new_row_df = pd.DataFrame({'year': [year], 'month': [month], 'day': [day], 'hour': [hour]})
        future_df = pd.concat([future_df, new_row_df], ignore_index=True)

    future_df_int = future_df.astype(int)
    predicted_charging_power = loaded_model.predict(future_df_int)
    return  np.round(predicted_charging_power, decimals=2)
