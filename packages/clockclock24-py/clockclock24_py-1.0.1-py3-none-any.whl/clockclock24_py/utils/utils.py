import random
import time
import threading
from typing import List, Dict, Any, Callable, Optional, Tuple, Union

def get_random_number(max_val: int, min_val: int = 1) -> int:
    """Generate a random number between min_val and max_val"""
    return random.randint(min_val, max_val)

def get_random_boolean() -> bool:
    """Generate a random boolean value"""
    return bool(round(random.random()))

def get_max_animation_time(timer: List[List[List[Dict[str, Any]]]]) -> int:
    """Get the maximum animation time from all clocks in the timer"""
    max_time = 0
    for number in timer:
        for line in number:
            for clock in line:
                anim_time = clock.get("animation_time", 0)
                if anim_time > max_time:
                    max_time = anim_time
    return max_time

class Timeout:
    """A class to handle timeouts with promises"""
    
    def __init__(self, time_ms: int):
        self.time_ms = time_ms
        self.is_cancelled = False
        self.is_completed = False
        self.callbacks = []
        self.error_callbacks = []
        
    def start(self):
        """Start the timeout"""
        def run():
            if not self.is_cancelled:
                time.sleep(self.time_ms / 1000)
                if not self.is_cancelled:
                    self.is_completed = True
                    for callback in self.callbacks:
                        callback()
        
        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()
        return self
        
    def cancel(self):
        """Cancel the timeout"""
        if not self.is_completed:
            self.is_cancelled = True
            for callback in self.error_callbacks:
                callback()
                
    def then(self, callback: Callable[[], None]):
        """Add a callback to be executed when the timeout completes"""
        if self.is_completed:
            callback()
        else:
            self.callbacks.append(callback)
        return self
        
    def catch(self, callback: Callable[[], None]):
        """Add a callback to be executed when the timeout is cancelled"""
        if self.is_cancelled:
            callback()
        else:
            self.error_callbacks.append(callback)
        return self

def start_timeout(time_ms: int) -> Timeout:
    """Start a timeout with the given time in milliseconds"""
    return Timeout(time_ms).start()

def run_sequences(sequence_functions: List[Callable[[], Timeout]]) -> Timeout:
    """Run a sequence of timeout functions one after another"""
    if not sequence_functions:
        timeout = Timeout(0)
        timeout.is_completed = True
        return timeout
        
    current_timeout = sequence_functions[0]()
    
    for i in range(1, len(sequence_functions)):
        current_timeout = current_timeout.then(lambda idx=i: sequence_functions[idx]())
        
    return current_timeout 