from typing import List, Dict, Any, Optional, Tuple, Union
import copy

from clockclock24_py.constants.config import ANIMATION_DELAY
from clockclock24_py.utils.timers import get_time_timer, get_timers
from clockclock24_py.utils.utils import get_random_boolean

NB_NUMBERS = 4
MIN_ROTATION = 180

def is_neg(num: float) -> bool:
    """Check if a number is negative"""
    return num < 0

def round_rest(rest_rotation: float) -> float:
    """Round the rotation value"""
    rest_round = abs(rest_rotation)
    round_val = rest_round - 360 if rest_round >= 360 + MIN_ROTATION else rest_round
    return -round_val if is_neg(rest_rotation) else round_val

def get_start_position(start: float) -> float:
    """Get the normalized start position"""
    if is_neg(start):
        return 360 + (start % 360)
    return start % 360

def get_min_value(rest: float) -> float:
    """Get the minimum rotation value"""
    return 360 if rest == 0 else rest

def rotate(start: float, end: float) -> float:
    """Calculate rotation in clockwise direction"""
    return start + round_rest(360 - (get_start_position(start) - end))

def rotate_reverse(start: float, end: float) -> float:
    """Calculate rotation in counter-clockwise direction"""
    return start + round_rest(-get_min_value(get_start_position(start)) + (end - 360))

def update_clocks_properties(numbers: List[List[List[Dict[str, Any]]]], 
                           callback: callable) -> List[List[List[Dict[str, Any]]]]:
    """Update all clocks in the timer using the provided callback"""
    result = copy.deepcopy(numbers)
    for number_idx, number in enumerate(result):
        for line_idx, line in enumerate(number):
            for clock_idx, clock in enumerate(line):
                result[number_idx][line_idx][clock_idx] = callback(
                    clock, number_idx * 2 + clock_idx, line_idx
                )
    return result

def set_clock_delay(clock: Dict[str, Any], x_pos: int, animation_time: int, 
                   delay: int = 0) -> Dict[str, Any]:
    """Set the animation delay for a clock"""
    animation_delay = x_pos * delay
    result = copy.deepcopy(clock)
    result["animation_delay"] = animation_delay
    result["animation_time"] = animation_time + NB_NUMBERS * delay - animation_delay
    return result

def compute_delays(timer: List[List[List[Dict[str, Any]]]], animation_time: int, 
                  delay: Optional[int] = None, rtl: bool = False) -> List[List[List[Dict[str, Any]]]]:
    """Compute animation delays for all clocks"""
    def callback(clock, x_pos, _):
        actual_x_pos = NB_NUMBERS * 2 - x_pos if rtl else x_pos
        return set_clock_delay(clock, actual_x_pos, animation_time, delay or 0)
    
    return update_clocks_properties(timer, callback)

def compute_animation_type(timer: List[List[List[Dict[str, Any]]]], 
                         animation_type: str) -> List[List[List[Dict[str, Any]]]]:
    """Set animation type for all clocks"""
    def callback(clock, _, __):
        result = copy.deepcopy(clock)
        result["animation_type"] = animation_type
        return result
    
    return update_clocks_properties(timer, callback)

def rotate_clock(clock: Dict[str, Any], current_clock: Dict[str, Any], 
                is_minutes_reversed: bool = False) -> Dict[str, Any]:
    """Calculate rotation for a clock"""
    result = copy.deepcopy(clock)
    
    current_hours = current_clock["hours"]
    current_minutes = current_clock["minutes"]
    
    result["hours"] = rotate(current_hours, clock["hours"])
    
    if is_minutes_reversed:
        result["minutes"] = rotate_reverse(current_minutes, clock["minutes"])
    else:
        result["minutes"] = rotate(current_minutes, clock["minutes"])
        
    return result

def compute_rotation(timer: List[List[List[Dict[str, Any]]]], 
                    current_timer: List[List[List[Dict[str, Any]]]], 
                    is_minutes_reversed: bool = False) -> List[List[List[Dict[str, Any]]]]:
    """Compute rotation for all clocks"""
    def callback(clock, x_pos, y_pos):
        number_idx = x_pos // 2
        clock_idx = x_pos % 2
        current_clock = current_timer[number_idx][y_pos][clock_idx]
        return rotate_clock(clock, current_clock, is_minutes_reversed)
    
    return update_clocks_properties(timer, callback)

def reset_clock(clock: Dict[str, Any]) -> Dict[str, Any]:
    """Reset a clock to its base state"""
    result = copy.deepcopy(clock)
    result["hours"] = result["hours"] % 360
    result["minutes"] = result["minutes"] % 360
    result["animation_time"] = 0
    result["animation_delay"] = 0
    return result

def reset_timer(timer: List[List[List[Dict[str, Any]]]]) -> List[List[List[Dict[str, Any]]]]:
    """Reset all clocks in a timer"""
    return update_clocks_properties(timer, lambda c, _, __: reset_clock(c))

class Sequence:
    """A sequence of timer animations"""
    
    def __init__(self, timer, seq_type="shape", animation_time=0, delay=0, 
                ltr=True, is_reverse=False, animation_type=None):
        self.timer = timer
        self.type = seq_type
        self.animation_time = animation_time
        self.delay = delay
        self.ltr = not ltr
        self.is_reverse = is_reverse
        self.animation_type = animation_type

def compute_timer(seq: Sequence, current_timer: List[List[List[Dict[str, Any]]]]) -> List[List[List[Dict[str, Any]]]]:
    """Compute the next timer state based on a sequence"""
    if seq.type == "wait":
        return compute_delays(current_timer, seq.animation_time, 0)
    
    next_timer_state = compute_rotation(
        seq.timer, 
        current_timer, 
        seq.is_reverse
    )
    
    if seq.animation_type:
        next_timer_state = compute_animation_type(next_timer_state, seq.animation_type)
        
    return compute_delays(next_timer_state, seq.animation_time, seq.delay, seq.ltr)

def compute_sequences(sequences: List[Sequence], 
                    last_timer: List[List[List[Dict[str, Any]]]]) -> List[List[List[Dict[str, Any]]]]:
    """Compute a sequence of timer states"""
    result = []
    current_timer = last_timer
    
    for seq in sequences:
        next_timer = compute_timer(seq, current_timer)
        result.append(next_timer)
        current_timer = next_timer
        
    return result

def get_wait_sequence(timer: List[List[List[Dict[str, Any]]]]) -> Sequence:
    """Create a wait sequence"""
    return Sequence(timer=timer, seq_type="wait", animation_time=3000)

def run(prev_timer: List[List[List[Dict[str, Any]]]], 
       options: Dict[str, Any]) -> List[List[List[Dict[str, Any]]]]:
    """Run the animation sequence"""
    animation_time = options.get("animation_time", 0)
    is_reverse = get_random_boolean()
    
    timer_sequences = []
    current_timers = get_timers(is_reverse)
    
    for index, timer in enumerate(current_timers):
        has_delay = index == 0 and get_random_boolean()
        
        # Determine animation type
        animation_type = None
        if index == 0 or (timer_sequences and timer_sequences[-1].type == "wait"):
            animation_type = "start"
        elif has_delay:
            animation_type = "end"
        
        # Create sequence
        sequence = Sequence(
            timer=timer,
            seq_type="shape",
            animation_time=animation_time,
            delay=ANIMATION_DELAY if index == 0 and get_random_boolean() else 0,
            is_reverse=is_reverse,
            animation_type=animation_type
        )
        
        timer_sequences.append(sequence)
        
        # Add wait sequence if needed
        if has_delay:
            timer_sequences.append(get_wait_sequence(timer))
    
    # Add final time sequence
    timer_sequences.append(
        Sequence(
            timer=get_time_timer(),
            seq_type="time",
            animation_time=animation_time,
            is_reverse=is_reverse,
            animation_type="end"
        )
    )
    
    return compute_sequences(timer_sequences, prev_timer) 