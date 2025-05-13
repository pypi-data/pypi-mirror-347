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
    GLOBAL_PADDING_MOBILE_CLOCK
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
        self.clock_size = self.get_clock_size()
        
        # Create the main frame
        self.frame = tk.Frame(root, bg="#141414")
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Create the canvas
        self.canvas = tk.Canvas(
            self.frame,
            bg="#141414",
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Create the instruction label
        self.instruction_label = tk.Label(
            self.frame,
            text="Press the [space] bar to animate the clock",
            fg="#141414",
            bg="#e8e8e8",
            font=("Helvetica", 11)
        )
        self.instruction_label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)
        
        # Create the footer label
        self.footer_label = tk.Label(
            self.frame,
            text="Made with ❤️ by TBOY1337 • Github",
            fg="#141414",
            bg="#e8e8e8",
            font=("Helvetica", 10)
        )
        self.footer_label.place(relx=0.5, rely=0.95, anchor=tk.CENTER)
        
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
        screen_width = self.root.winfo_screenwidth()
        padding = GLOBAL_PADDING_CLOCK if screen_width >= 1100 else GLOBAL_PADDING_MOBILE_CLOCK
        
        available_width = screen_width - 2 * padding - 2 * CLOCK_PADDING * NB_COLUMN_CLOCKS
        clock_size = available_width / NB_COLUMN_CLOCKS
        
        return min(clock_size, CLOCK_MAX_SIZE)
        
    def create_numbers(self):
        """Create the four numbers that display the time"""
        # Clear existing numbers
        self.numbers = []
        
        # Calculate the total width and height of the display
        number_width = 2 * (self.clock_size + CLOCK_PADDING)
        number_height = 3 * (self.clock_size + CLOCK_PADDING)
        total_width = 4 * number_width
        total_height = number_height
        
        # Calculate the starting position
        start_x = (self.root.winfo_width() - total_width) / 2
        start_y = (self.root.winfo_height() - total_height) / 2
        
        # Create the four numbers
        for i in range(4):
            x = start_x + i * number_width
            y = start_y
            
            number = Number(
                canvas=self.canvas,
                x=x,
                y=y,
                number_data=self.timer[i],
                clock_size=self.clock_size
            )
            
            self.numbers.append(number)
            
    def update_numbers(self):
        """Update the numbers with the current timer data"""
        for i, number in enumerate(self.numbers):
            number.update(self.timer[i])
            
    def on_resize(self, event):
        """Handle window resize event"""
        # Recalculate clock size
        self.clock_size = self.get_clock_size()
        
        # Redraw the numbers
        self.canvas.delete("all")
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