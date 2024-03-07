from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

class EvForecastForm(tk.Toplevel):
    def __init__(self, parent, charging_station):
        super().__init__(parent)
        self.title("EV forecast")
        self.geometry("800x800")
        self.charging_station = charging_station
        
        forecast_detail = self.charging_station.ev_forecast

        # Create a figure and axis for the plot
        fig, ax = plt.subplots()
        
        cur_time = pd.to_datetime(self.charging_station.time+":00")
        print(cur_time)
        hour = []
        for i in range(24):
            # hour.append(cur_time + pd.to_timedelta(hours = i))
            new_time = ((cur_time) + timedelta(hours=i)).time()
            hour.append(new_time.strftime('%H')+":00")  
        print(hour)
        # Plot the forecast data
        ax.plot(hour, forecast_detail, marker='o', linestyle='-')
        ax.set_xlabel('Hours')
        ax.set_ylabel('Energy Demand (kWh)')
        ax.set_title('EV Forecast for the Next 24 Hours')

        plt.xticks(rotation=45) 

        # Embed the plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # for i in range(1, 25):
        #     ttk.Label(self, text=f"Next {i} hour: {forecast_detail[i-1]} kWh").pack(pady=5)

# Example usage:
# charging_station = ChargingStation()  # Replace with your ChargingStation class
# app = EvForecastForm(parent, charging_station)
# app.mainloop()
