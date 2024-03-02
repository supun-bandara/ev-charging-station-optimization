import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

class emptyBatteryUI:
    def __init__(self, root, style, charger_id, row, col,current_soc,required_soc,arrival_time,departure_time,battery_capacity,charging_power,charging_price):
        self.root = root

        # Create a frame for each battery
        style.configure("battery.TFrame", background="#CBC3E3")
        
        self.frame = ttk.Frame(root, padding="10", style="battery.TFrame")
        self.frame.grid(row=row, column=col, padx=5, pady=5)
        
        #battery id
        self.charger_id=charger_id        

               # Change the background color of the root window
        self.root.configure(background='#CBC3E3')

        self.font=("Hack Regular", 10,)
        
        # Draw the battery outline
        self.canvas = tk.Canvas(self.frame, width=200, height=200, bg="#CBC3E3", highlightthickness=2)
        
        if self.charger_id<=3:            
            emptyBatteryUI.dc_charger_icon(self)
        
        elif self.charger_id>3:
            emptyBatteryUI.ac_charger_icon(self)
       
    def dc_charger_icon(self):

            print("succes")
                
            self.charger_icon_path = "gui\icons\DC-charger.png"  # Replace with the actual path to your charger icon
            self.charger_icon = tk.PhotoImage(file=self.charger_icon_path)
            
            x_center = self.canvas.winfo_reqwidth() // 2
            y_center = self.canvas.winfo_reqheight() // 2
                       
            self.canvas.create_image(x_center, y_center, image=self.charger_icon)
            self.canvas.pack()
            
            self.label_charge = ttk.Label(self.frame, text=f"        ", background="#CBC3E3",
                                        foreground="black", font=self.font)
            self.label_charge.pack()
            self.label_charge = ttk.Label(self.frame, text=f"DC Charger: {self.charger_id}", background="#CBC3E3",
                                        foreground="black", font=self.font)
            self.label_charge.pack()
                      
    def ac_charger_icon(self):
         
            self.charger_icon_path = "gui\icons\AC-chargers.png"  # Replace with the actual path to your charger icon
            self.charger_icon = tk.PhotoImage(file=self.charger_icon_path)
            
            x_center = self.canvas.winfo_reqwidth() // 2
            y_center = self.canvas.winfo_reqheight() // 2
            self.canvas.create_image(x_center, y_center, image=self.charger_icon) 
            self.canvas.pack()
            
            self.label_charge = ttk.Label(self.frame, text=f"        ", background="#CBC3E3",
                                        foreground="black", font=self.font)
            self.label_charge.pack()
            self.label_charge = ttk.Label(self.frame, text=f"AC Charger: {self.charger_id}", background="#CBC3E3",
                                        foreground="black", font=self.font)
            self.label_charge.pack()        
