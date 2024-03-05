# for ev forecast details

import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

class EvForecastForm(tk.Toplevel):
    def __init__(self, parent, charging_station):
        super().__init__(parent)
        self.title("EV forcast ")
        self.geometry("200x180")
        self.charging_station = charging_station
        
        forcast_detail = self.charging_station.Grid_price_forecast
        
        for i in range(1,7):
            ttk.Label(self, text=f"Next {i} hour: {forcast_detail[i-1]}kW").pack(pady=5)
