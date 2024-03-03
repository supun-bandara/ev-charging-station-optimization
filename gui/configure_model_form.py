# not important right now

import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

class ConfigureModelForm(tk.Toplevel):
    def __init__(self, parent): 
        super().__init__(parent)
        self.title("Configure Model")
        self.geometry("200x150")

        # Create buttons for model configuration
        ttk.Button(self, text="Train Model", command=self.train_model).pack(pady=5)
        ttk.Button(self, text="Test Model", command=self.test_model).pack(pady=5)
        ttk.Button(self, text="Save Model", command=self.save_model).pack(pady=5)
        ttk.Button(self, text="Show Plots", command=self.show_plots).pack(pady=5)

    def train_model(self):
        # Implement the logic for training the model
        messagebox.showinfo("Train Model", "Model training functionality to be implemented.")

    def test_model(self):
        # Implement the logic for testing the model
        messagebox.showinfo("Test Model", "Model testing functionality to be implemented.")

    def save_model(self):
        # Implement the logic for saving the model
        messagebox.showinfo("Save Model", "Model saving functionality to be implemented.")

    def show_plots(self):
        # Implement the logic for showing plots
        messagebox.showinfo("Show Plots", "Plot display functionality to be implemented.")
