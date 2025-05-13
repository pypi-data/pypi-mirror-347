import tkinter as tk
from clockclock24_py.components.clockclock24 import ClockClock24

def main():
    """Main function to run the ClockClock24 application"""
    # Create the root window
    root = tk.Tk()
    root.title("ClockClock24")
    
    # Set window size and position
    window_width = 800
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # Set window background color
    root.configure(bg="#e8e8e8")
    
    # Create the ClockClock24 component
    clock_clock_24 = ClockClock24(root)
    
    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main() 