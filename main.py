import tkinter as tk
from PIL import Image, ImageTk

class MovableImage(tk.Tk):
    def __init__(self, image_path):
        super().__init__()
        self.title("Movable Image")

        # Load the image
        self.image = Image.open(image_path)
        self.photo = ImageTk.PhotoImage(self.image)

        # Create a canvas and add the image to it
        self.canvas = tk.Canvas(self, width=self.image.width, height=self.image.height)
        self.image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        self.canvas.pack()

        # Bind mouse events for dragging
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)

    def on_press(self, event):
        # Record the initial position of the mouse
        self.initial_x = event.x
        self.initial_y = event.y

    def on_drag(self, event):
        # Calculate the difference
        dx = event.x - self.initial_x
        dy = event.y - self.initial_y

        # Update the position
        self.canvas.move(self.image_id, dx, dy)

        # Update the initial position
        self.initial_x = event.x
        self.initial_y = event.y

if __name__ == "__main__":
    image_path = 'a-teenager-playing-games-with-headphones-with-blac.png'  # Replace with your image path
    app = MovableImage(image_path)
    app.mainloop()
