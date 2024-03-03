import tkinter as tk
from PIL import Image, ImageTk

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter Canvas with Transparent PNG Image")

        # Create a canvas with a transparent PNG image
        image_path = "icons/AC-chargers.png"  # Change this to the actual path of your transparent PNG image file

        # Open the image using Pillow
        image = Image.open(image_path)

        # Create a mask to handle transparency
        mask = Image.new("L", image.size, 255)  # Create a white mask
        image.putalpha(mask)

        # Convert the image to a format compatible with Tkinter
        tk_image = ImageTk.PhotoImage(image)

        # Create a canvas
        self.canvas = tk.Canvas(self.root, width=tk_image.width(), height=tk_image.height())
        self.canvas.grid(row=0, column=0, padx=10, pady=10)

        # Display the image on the canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
