import tkinter as tk
from typing import Dict, Any

class Needle:
    """A needle component for the clock"""
    
    def __init__(self, canvas: tk.Canvas, height: float, width: float, x: float, y: float):
        """
        Initialize a needle
        
        Args:
            canvas: The canvas to draw on
            height: The height/length of the needle
            width: The width of the needle
            x: The x position of the needle base
            y: The y position of the needle base
        """
        self.canvas = canvas
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.needle = None
        self.draw()
        
    def draw(self):
        """Draw the needle on the canvas"""
        # Calculate coordinates for the rectangle
        x1 = self.x - self.width / 2
        y1 = self.y
        x2 = self.x + self.width / 2
        y2 = self.y + self.height
        
        # Create the needle as a rectangle with rounded top
        self.needle = self.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill="#c9c9c9",  # Needle color
            outline="",
            width=0
        )
        
        # Add a small shadow effect
        self.canvas.create_line(
            x1, y1, x1, y2,
            fill="#b0b0b0",
            width=1
        )
        
    def update(self, x: float, y: float):
        """Update the position of the needle"""
        self.x = x
        self.y = y
        self.canvas.delete(self.needle)
        self.draw() 