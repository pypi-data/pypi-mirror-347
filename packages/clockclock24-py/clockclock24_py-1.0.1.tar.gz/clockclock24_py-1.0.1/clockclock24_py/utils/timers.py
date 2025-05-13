import datetime
import random
from typing import List, Dict, Any

from clockclock24_py.constants import numbers
from clockclock24_py.constants import shapes

def get_arr_time() -> List[int]:
    """Get the current time as an array of digits"""
    time_now = datetime.datetime.now()
    time_str = time_now.strftime("%H%M")
    return [int(digit) for digit in time_str]

def get_time_timer() -> List[List[List[Dict[str, Any]]]]:
    """Get the current time in a timer format"""
    return [numbers.NUMBERS[digit] for digit in get_arr_time()]

def get_random_shaped_timer(shape_type: str) -> List[List[List[Dict[str, Any]]]]:
    """Get a random shape from the specified shape type"""
    shape_list = shapes.SHAPE_TYPES[shape_type]
    random_index = random.randint(0, len(shape_list) - 1)
    return shape_list[random_index]

def get_same_shape(count: int, shape_type: str) -> List[List[List[List[Dict[str, Any]]]]]:
    """Get multiple instances of the same shape"""
    shape = get_random_shaped_timer(shape_type)
    return [shape] * count

def get_different_shape(count: int, shape_type: str) -> List[List[List[List[Dict[str, Any]]]]]:
    """Get multiple different shapes of the same type"""
    return [get_random_shaped_timer(shape_type) for _ in range(count)]

def get_timers(is_same: bool, count: int = 2) -> List[List[List[List[Dict[str, Any]]]]]:
    """Get a list of timer configurations based on the is_same parameter"""
    shape_type = "SYMMETRICAL" if is_same else "LINEAR"
    
    if is_same:
        return get_same_shape(count, shape_type)
    else:
        return get_different_shape(count, shape_type) 