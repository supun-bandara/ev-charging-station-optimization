import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def button_clicked():
    #print("Button Clicked")

# Create Tkinter window
root = tk.Tk()
root.title("Themed Button with Icon")

# Load the image
icon_image = Image.open("icons/AC-chargers.png")
icon_photo = ImageTk.PhotoImage(icon_image)

# Create a themed button with the icon
style = ttk.Style()
style.configure("TButton", padding=5, relief="flat", background="#ccc")

button = ttk.Button(root, text="Click Me", image=icon_photo, compound=tk.LEFT, command=button_clicked, style="TButton")

# Pack the button and run the Tkinter main loop
button.pack(pady=10)
root.mainloop()
