import tkinter as tk
import math
from typing import Dict, Any, Optional

from clockclock24_py.components.needle import Needle
from clockclock24_py.constants.config import (
    ANIMATION_START_TIMING,
    ANIMATION_END_TIMING,
    ANIMATION_DEFAULT_TIMING,
    ANIMATION_TIMING_CONFIG
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
        self.draw()
        
    def draw(self):
        """Draw the clock on the canvas"""
        # Draw the clock face (circle)
        self.clock_face = self.canvas.create_oval(
            self.x - self.size/2, self.y - self.size/2,
            self.x + self.size/2, self.y + self.size/2,
            fill="#141414",  # Clock background color
            outline="#1a1a1a",
            width=1
        )
        
        # Calculate needle dimensions
        needle_width = self.size / 9
        hours_needle_height = self.size / 2
        minutes_needle_height = hours_needle_height - 4
        
        # Create the needles
        self.hours_needle = Needle(
            canvas=self.canvas,
            height=hours_needle_height,
            width=needle_width,
            x=self.x,
            y=self.y
        )
        
        self.minutes_needle = Needle(
            canvas=self.canvas,
            height=minutes_needle_height,
            width=needle_width,
            x=self.x,
            y=self.y
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
        # Convert angle to radians and adjust for canvas coordinates
        radians = math.radians(angle - 90)  # -90 to adjust for canvas coordinate system
        
        # Calculate the new position
        needle_length = needle.height
        end_x = self.x + needle_length * math.cos(radians)
        end_y = self.y + needle_length * math.sin(radians)
        
        # Update the needle
        self.canvas.delete(needle.needle)
        
        # Create a new rotated needle
        needle.x = self.x
        needle.y = self.y
        
        # Calculate the points for the rotated rectangle
        width = needle.width
        height = needle.height
        
        # Calculate the four corners of the rectangle
        corners = [
            (-width/2, 0),
            (width/2, 0),
            (width/2, height),
            (-width/2, height)
        ]
        
        # Rotate each corner
        rotated_corners = []
        for corner_x, corner_y in corners:
            # Rotate the point
            rx = corner_x * math.cos(radians) - corner_y * math.sin(radians)
            ry = corner_x * math.sin(radians) + corner_y * math.cos(radians)
            
            # Translate to the center of the clock
            rx += self.x
            ry += self.y
            
            rotated_corners.append((rx, ry))
        
        # Create the polygon
        needle.needle = self.canvas.create_polygon(
            *[coord for point in rotated_corners for coord in point],
            fill="#c9c9c9",
            outline="",
            width=0
        )
        
        # Add a subtle shadow effect
        shadow_corners = rotated_corners[:2]  # Just use the first two corners for the shadow line
        self.canvas.create_line(
            *[coord for point in shadow_corners for coord in point],
            fill="#b0b0b0",
            width=1
        )