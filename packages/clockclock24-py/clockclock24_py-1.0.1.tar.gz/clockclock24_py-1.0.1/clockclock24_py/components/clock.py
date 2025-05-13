import tkinter as tk
import math
from typing import Dict, Any, Optional

from clockclock24_py.components.needle import Needle
from clockclock24_py.constants.config import (
    ANIMATION_START_TIMING,
    ANIMATION_END_TIMING,
    ANIMATION_DEFAULT_TIMING,
    ANIMATION_TIMING_CONFIG,
    CLOCK_BACKGROUND_COLOR,
    NEEDLE_BACKGROUND_COLOR
)

class Clock:
    """A clock component with two needles"""
    
    def __init__(self, canvas: tk.Canvas, x: float, y: float, size: float, 
                clock_data: Dict[str, Any]):
        """
        Initialize a clock
        
        Args:
            canvas: The canvas to draw on
            x: The x position of the clock
            y: The y position of the clock
            size: The size of the clock
            clock_data: The clock data with hours, minutes, animation settings
        """
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        self.clock_data = clock_data
        self.hours_needle = None
        self.minutes_needle = None
        self.clock_face = None
        self.center_dot = None
        self.draw()
        
    def draw(self):
        """Draw the clock on the canvas"""
        # Draw the clock face (circle)
        self.clock_face = self.canvas.create_oval(
            self.x - self.size/2, self.y - self.size/2,
            self.x + self.size/2, self.y + self.size/2,
            fill=CLOCK_BACKGROUND_COLOR,
            outline="#1a1a1a",
            width=1
        )
        
        # Calculate needle dimensions
        needle_width = max(2, self.size / 25)  # Ensure needle is visible
        hours_needle_length = self.size * 0.35  # Shorter hour hand
        minutes_needle_length = self.size * 0.45  # Longer minute hand
        
        # Create the needles
        self.hours_needle = Needle(
            canvas=self.canvas,
            height=hours_needle_length,
            width=needle_width,
            x=self.x,
            y=self.y
        )
        
        self.minutes_needle = Needle(
            canvas=self.canvas,
            height=minutes_needle_length,
            width=needle_width,
            x=self.x,
            y=self.y
        )
        
        # Draw center dot
        dot_size = max(3, self.size / 20)
        self.center_dot = self.canvas.create_oval(
            self.x - dot_size/2, self.y - dot_size/2,
            self.x + dot_size/2, self.y + dot_size/2,
            fill=NEEDLE_BACKGROUND_COLOR,
            outline=""
        )
        
        # Set initial rotation
        self.update(self.clock_data)
        
    def update(self, clock_data: Dict[str, Any]):
        """Update the clock with new data"""
        self.clock_data = clock_data
        
        # Get rotation angles
        hours_angle = self.clock_data.get("hours", 0)
        minutes_angle = self.clock_data.get("minutes", 0)
        
        # Rotate the needles
        self.rotate_needle(self.hours_needle, hours_angle)
        self.rotate_needle(self.minutes_needle, minutes_angle)
        
    def rotate_needle(self, needle: Needle, angle: float):
        """Rotate a needle to the specified angle"""
        # Delete the old needle
        if needle.needle:
            self.canvas.delete(needle.needle)
        
        # Convert angle to radians and adjust for canvas coordinates
        # In tkinter, 0 degrees is east, and angles increase clockwise
        # We need to adjust by -90 to make 0 degrees point north
        radians = math.radians(angle - 90)
        
        # Calculate the needle endpoint
        end_x = self.x + needle.height * math.cos(radians)
        end_y = self.y + needle.height * math.sin(radians)
        
        # Draw a simple line for the needle
        needle.needle = self.canvas.create_line(
            self.x, self.y, end_x, end_y,
            fill=NEEDLE_BACKGROUND_COLOR,
            width=needle.width,
            capstyle=tk.ROUND
        )