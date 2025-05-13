import tkinter as tk
from typing import List, Dict, Any

from clockclock24_py.components.clock import Clock

class Number:
    """A number component composed of 6 clocks arranged in a 3x2 grid"""
    
    def __init__(self, canvas: tk.Canvas, x: float, y: float, 
                number_data: List[List[Dict[str, Any]]], clock_size: float):
        """
        Initialize a number
        
        Args:
            canvas: The canvas to draw on
            x: The x position of the top-left corner of the number
            y: The y position of the top-left corner of the number
            number_data: The data for the 6 clocks that make up the number
            clock_size: The size of each clock
        """
        self.canvas = canvas
        self.x = x
        self.y = y
        self.number_data = number_data
        self.clock_size = clock_size
        self.clocks = []
        self.draw()
        
    def draw(self):
        """Draw the number on the canvas"""
        padding = 3  # Small padding between clocks
        
        for line_idx, line in enumerate(self.number_data):
            for clock_idx, clock_data in enumerate(line):
                # Calculate position for this clock
                clock_x = self.x + clock_idx * (self.clock_size + padding) + self.clock_size / 2
                clock_y = self.y + line_idx * (self.clock_size + padding) + self.clock_size / 2
                
                # Create the clock
                clock = Clock(
                    canvas=self.canvas,
                    x=clock_x,
                    y=clock_y,
                    size=self.clock_size,
                    clock_data=clock_data
                )
                
                self.clocks.append(clock)
                
    def update(self, number_data: List[List[Dict[str, Any]]]):
        """Update the number with new data"""
        self.number_data = number_data
        
        clock_index = 0
        for line_idx, line in enumerate(self.number_data):
            for clock_idx, clock_data in enumerate(line):
                self.clocks[clock_index].update(clock_data)
                clock_index += 1 