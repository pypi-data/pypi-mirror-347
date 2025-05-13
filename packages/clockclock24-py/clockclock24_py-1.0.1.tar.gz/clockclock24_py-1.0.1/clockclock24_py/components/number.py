import tkinter as tk
from typing import List, Dict, Any

from clockclock24_py.components.clock import Clock
from clockclock24_py.constants.config import CLOCK_PADDING

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
        # Clear any existing clocks
        self.clocks = []
        
        # Use the constant padding between clocks
        padding = CLOCK_PADDING
        
        # Ensure we have the correct data structure (3 rows, 2 columns)
        if not self.number_data or len(self.number_data) != 3:
            # Default to empty data if invalid
            self.number_data = [[{}, {}], [{}, {}], [{}, {}]]
            
        # Draw the clocks in a 3x2 grid
        for row_idx, row in enumerate(self.number_data):
            for col_idx, clock_data in enumerate(row):
                if col_idx < 2:  # Ensure we only have 2 columns
                    # Calculate position for this clock (center of the clock)
                    clock_x = self.x + col_idx * (self.clock_size + padding) + self.clock_size / 2
                    clock_y = self.y + row_idx * (self.clock_size + padding) + self.clock_size / 2
                    
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
        
        # Ensure we have the correct number of clocks
        if len(self.clocks) != 6:
            # Redraw if the number of clocks is incorrect
            self.draw()
            return
            
        # Update each clock with its new data
        clock_index = 0
        for row_idx, row in enumerate(self.number_data):
            for col_idx, clock_data in enumerate(row):
                if col_idx < 2 and clock_index < len(self.clocks):  # Safety check
                    self.clocks[clock_index].update(clock_data)
                    clock_index += 1 