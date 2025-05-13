import tkinter as tk
import threading
import time
from typing import List, Dict, Any, Optional
from datetime import datetime

from clockclock24_py.components.number import Number
from clockclock24_py.constants.config import (
    NB_COLUMN_CLOCKS,
    ANIMATION_TIME,
    CLOCK_MAX_SIZE,
    CLOCK_PADDING,
    GLOBAL_PADDING_CLOCK,
    GLOBAL_PADDING_MOBILE_CLOCK,
    CLOCK_BACKGROUND_COLOR,
    BACKGROUND_COLOR
)
from clockclock24_py.utils.timers import get_time_timer
from clockclock24_py.utils.utils import get_max_animation_time, start_timeout, run_sequences
from clockclock24_py.utils.engine import run, reset_timer

class ClockClock24:
    """The main ClockClock24 component that displays the time using 24 clocks"""
    
    def __init__(self, root: tk.Tk):
        """
        Initialize the ClockClock24 component
        
        Args:
            root: The Tkinter root window
        """
        self.root = root
        self.timer = get_time_timer()
        self.is_running = False
        self.timeout = None
        self.animation_time = ANIMATION_TIME
        
        # Create the main frame
        self.frame = tk.Frame(root, bg=CLOCK_BACKGROUND_COLOR)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Create the canvas
        self.canvas = tk.Canvas(
            self.frame,
            bg=CLOCK_BACKGROUND_COLOR,
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Create the instruction label
        self.instruction_label = tk.Label(
            self.frame,
            text="Press the [space] bar to animate the clock",
            fg="#e8e8e8",
            bg=CLOCK_BACKGROUND_COLOR,
            font=("Helvetica", 11)
        )
        self.instruction_label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)
        
        # Create the footer label
        self.footer_label = tk.Label(
            self.frame,
            text="Made with ❤️ by TBOY1337 • Github",
            fg="#e8e8e8",
            bg=CLOCK_BACKGROUND_COLOR,
            font=("Helvetica", 10)
        )
        self.footer_label.place(relx=0.5, rely=0.95, anchor=tk.CENTER)
        
        # Calculate initial clock size
        self.clock_size = self.get_clock_size()
        
        # Create the numbers
        self.numbers = []
        self.create_numbers()
        
        # Bind keyboard events
        self.root.bind("<space>", lambda e: self.start_cycle())
        
        # Start the animation cycle
        self.start_next_cycle(1000)
        
        # Handle window resize
        self.root.bind("<Configure>", self.on_resize)
        
    def get_clock_size(self) -> float:
        """Calculate the appropriate clock size based on window dimensions"""
        window_width = self.root.winfo_width() or 800  # Default to 800 if not yet configured
        window_height = self.root.winfo_height() or 600  # Default to 600 if not yet configured
        
        # Use the smaller dimension to ensure clocks fit
        min_dimension = min(window_width, window_height)
        
        # Calculate available width for all 4 numbers (each with 2 clocks side by side)
        # Total width = 8 clocks in a row + spacing between hours and minutes
        horizontal_clocks = 8  # 4 digits × 2 clocks per digit
        horizontal_padding = GLOBAL_PADDING_CLOCK * 2  # Left and right padding
        horizontal_spacing = CLOCK_PADDING * (horizontal_clocks - 1)  # Between clocks
        colon_spacing = CLOCK_PADDING * 4  # Extra space for colon between hours and minutes
        
        available_width = window_width - horizontal_padding - horizontal_spacing - colon_spacing
        clock_size_width = available_width / horizontal_clocks
        
        # Calculate available height for 3 clocks vertically
        vertical_clocks = 3  # 3 clocks per digit vertically
        vertical_padding = GLOBAL_PADDING_CLOCK * 2  # Top and bottom padding
        vertical_spacing = CLOCK_PADDING * (vertical_clocks - 1)  # Between clocks
        label_space = 80  # Space for labels
        
        available_height = window_height - vertical_padding - vertical_spacing - label_space
        clock_size_height = available_height / vertical_clocks
        
        # Use the smaller size to ensure everything fits
        clock_size = min(clock_size_width, clock_size_height, CLOCK_MAX_SIZE)
        
        return max(clock_size, 30)  # Ensure minimum size of 30 pixels
        
    def create_numbers(self):
        """Create the four numbers that display the time"""
        # Clear existing numbers and canvas
        self.canvas.delete("all")
        self.numbers = []
        
        # Calculate the total width and height of the display
        clock_size = self.clock_size
        number_width = 2 * (clock_size + CLOCK_PADDING)
        number_height = 3 * (clock_size + CLOCK_PADDING)
        
        # Add spacing between hour and minute pairs (colon space)
        colon_spacing = clock_size
        
        # Calculate the starting position to center the entire display
        canvas_width = self.root.winfo_width()
        canvas_height = self.root.winfo_height()
        
        total_width = 4 * number_width + colon_spacing
        start_x = (canvas_width - total_width) / 2
        start_y = (canvas_height - number_height) / 2
        
        # Draw colon (two dots between hours and minutes)
        colon_x = start_x + 2 * number_width + colon_spacing/2
        dot_radius = clock_size / 8
        dot_spacing = clock_size / 3
        
        # Top dot of colon
        self.canvas.create_oval(
            colon_x - dot_radius, 
            start_y + number_height/2 - dot_spacing - dot_radius,
            colon_x + dot_radius, 
            start_y + number_height/2 - dot_spacing + dot_radius,
            fill="#e8e8e8",
            outline=""
        )
        
        # Bottom dot of colon
        self.canvas.create_oval(
            colon_x - dot_radius, 
            start_y + number_height/2 + dot_spacing - dot_radius,
            colon_x + dot_radius, 
            start_y + number_height/2 + dot_spacing + dot_radius,
            fill="#e8e8e8",
            outline=""
        )
        
        # Create the four numbers (HH:MM)
        for i in range(4):
            # Add extra spacing between hours and minutes (between digits 1 and 2)
            x_offset = 0
            if i >= 2:
                x_offset = colon_spacing
                
            x = start_x + i * number_width + x_offset
            y = start_y
            
            number = Number(
                canvas=self.canvas,
                x=x,
                y=y,
                number_data=self.timer[i],
                clock_size=clock_size
            )
            
            self.numbers.append(number)
            
    def update_numbers(self):
        """Update the numbers with the current timer data"""
        for i, number in enumerate(self.numbers):
            if i < len(self.timer):
                number.update(self.timer[i])
            
    def on_resize(self, event):
        """Handle window resize event"""
        # Only respond to window size changes, not other configure events
        if event.widget == self.root and (event.width != getattr(self, '_last_width', 0) or 
                                         event.height != getattr(self, '_last_height', 0)):
            self._last_width = event.width
            self._last_height = event.height
            
            # Recalculate clock size
            self.clock_size = self.get_clock_size()
            
            # Redraw the numbers
            self.create_numbers()
        
    def get_remaining_time(self) -> int:
        """Get the remaining time before the next minute change"""
        seconds_in_milli = datetime.now().second * 1000
        return 60 * 1000 - seconds_in_milli
        
    def start_next_cycle(self, time_ms: int):
        """Start the next animation cycle after the specified time"""
        self.timeout = start_timeout(time_ms)
        
        def on_timeout():
            self.start_cycle()
            
        self.timeout.then(on_timeout)
        
    def animate_timer(self, timer: List[List[List[Dict[str, Any]]]]) -> None:
        """Animate the timer with the new data"""
        self.timer = timer
        self.update_numbers()
        
        # Get the maximum animation time
        animation_time = get_max_animation_time(timer)
        
        # Return a timeout promise
        return start_timeout(animation_time)
        
    def start_cycle(self):
        """Start the animation cycle"""
        if self.is_running:
            return
            
        if self.timeout:
            self.timeout.cancel()
            self.timeout = None
            
        self.is_running = True
        
        # Run the animation sequence
        sequences = run(self.timer, {"animation_time": self.animation_time})
        
        # Create a list of functions to animate each sequence
        sequence_functions = []
        for timer in sequences:
            def create_animation_function(t):
                return lambda: self.animate_timer(t)
            sequence_functions.append(create_animation_function(timer))
        
        # Run the sequences
        timeout = run_sequences(sequence_functions)
        
        def on_complete():
            # Reset the timer
            if sequences:
                clear_timer = reset_timer(sequences[-1])
                self.timer = clear_timer
                self.update_numbers()
                
            # Start the next cycle
            self.start_next_cycle(self.get_remaining_time())
            self.is_running = False
            
        timeout.then(on_complete) 