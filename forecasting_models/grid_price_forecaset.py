# grid price forecast
# give inputs in minutes
# to be replaced with the API

import pandas as pd
from datetime import datetime, timedelta
import pickle
import xgboost
import numpy as np

def grid_price_forecast(ref):
    current_timestamp = pd.to_datetime("2024-02-02 " + ref)
    future_df = pd.DataFrame(columns=['year', 'month', 'day', 'hour', 'minute'])
    model_price = 'forecasting_models/trained_model_price.pkl'
    loaded_model = pickle.load(open(model_price, 'rb'))

    for i in range(13): # 13
        future_timestamp = current_timestamp + timedelta(minutes=i*15)
        year = future_timestamp.year
        month = future_timestamp.month
        day = future_timestamp.day
        hour = future_timestamp.hour
        minute = future_timestamp.minute
        new_row_df = pd.DataFrame({'year': [year], 'month': [month], 'day': [day], 'hour': [hour], 'minute': [minute]})
        future_df = pd.concat([future_df, new_row_df], ignore_index=True)

    future_df = future_df.astype(int)
    predicted_grid_price = loaded_model.predict(future_df)
    
    return np.round(predicted_grid_price, decimals=2)

print(grid_price_forecast('00:00'))