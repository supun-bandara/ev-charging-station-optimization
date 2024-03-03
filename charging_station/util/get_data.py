# read data to train the drl model in each timestep

import pandas as pd

def get_data(self):
    #print('Data')
    #print()
    ID = self.timestep
    price = self.df_price.iloc[ID:ID + 13]['price'].values
    ev_forecast = self.df_ev_forecast.iloc[ID:ID + 10:4]['Total_Energy'].values

    #print('get_data - price')

    '''price = self.df_price[self.df_price['ID'] == ID]['price'].values[0]

    price_data = self.df_price[self.df_price['ID'] == ID]['price'].values
    index_of_id = self.df_price[self.df_price['ID'] == ID].index[0]
    next_12_prices = self.df_price.iloc[index_of_id:index_of_id + 13]['price'].values
    result_array = price_data.tolist() + next_12_prices.tolist()'''

    new_evs = []

    if ID in self.df_station['Start_Time_Index'].values:
        rows = self.df_station.loc[self.df_station['Start_Time_Index'] == ID]
        for index, row in rows.iterrows():
            duration = row['Duration_Count']
            SOC = row['SOC_Level']
            Capacity = row['Battery_Capacity_kWh']
            energy_demand = (100-SOC)*Capacity/100
            new_evs.append([duration, energy_demand])
    
    #print('Data - price', price, 'new_evs', new_evs)
    #print()
    return price, new_evs, ev_forecast