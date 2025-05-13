import unittest
from unittest.mock import patch
import datetime

from clockclock24_py.utils.timers import (
    get_arr_time,
    get_time_timer,
    get_random_shaped_timer,
    get_same_shape,
    get_different_shape,
    get_timers
)

class TestTimers(unittest.TestCase):
    """Test cases for the timers module"""
    
    @patch('clockclock24_py.utils.timers.datetime')
    def test_get_arr_time(self, mock_datetime):
        """Test the get_arr_time function"""
        # Mock the datetime to return a fixed time
        mock_now = datetime.datetime(2023, 1, 1, 12, 34)
        mock_datetime.datetime.now.return_value = mock_now
        
        # The time should be 12:34, so the array should be [1, 2, 3, 4]
        self.assertEqual(get_arr_time(), [1, 2, 3, 4])
        
        # Test another time
        mock_now = datetime.datetime(2023, 1, 1, 9, 5)
        mock_datetime.datetime.now.return_value = mock_now
        
        # The time should be 09:05, so the array should be [0, 9, 0, 5]
        self.assertEqual(get_arr_time(), [0, 9, 0, 5])
    
    @patch('clockclock24_py.utils.timers.get_arr_time')
    def test_get_time_timer(self, mock_get_arr_time):
        """Test the get_time_timer function"""
        # Mock get_arr_time to return a fixed time array
        mock_get_arr_time.return_value = [1, 2, 3, 4]
        
        # Get the timer
        timer = get_time_timer()
        
        # Check that the timer has 4 numbers
        self.assertEqual(len(timer), 4)
        
        # Check that each number has 3 lines
        for number in timer:
            self.assertEqual(len(number), 3)
            
            # Check that each line has 2 clocks
            for line in number:
                self.assertEqual(len(line), 2)
                
                # Check that each clock has hours and minutes
                for clock in line:
                    self.assertIn("hours", clock)
                    self.assertIn("minutes", clock)
    
    def test_get_random_shaped_timer(self):
        """Test the get_random_shaped_timer function"""
        # Get a random timer of each type
        linear_timer = get_random_shaped_timer("LINEAR")
        symmetrical_timer = get_random_shaped_timer("SYMMETRICAL")
        
        # Check that the timers have the correct structure
        self.assertEqual(len(linear_timer), 4)
        self.assertEqual(len(symmetrical_timer), 4)
        
        for number in linear_timer + symmetrical_timer:
            self.assertEqual(len(number), 3)
            
            for line in number:
                self.assertEqual(len(line), 2)
                
                for clock in line:
                    self.assertIn("hours", clock)
                    self.assertIn("minutes", clock)
    
    def test_get_same_shape(self):
        """Test the get_same_shape function"""
        # Get multiple instances of the same shape
        shapes = get_same_shape(3, "LINEAR")
        
        # Check that we got the right number of shapes
        self.assertEqual(len(shapes), 3)
        
        # Check that all shapes are the same
        self.assertEqual(shapes[0], shapes[1])
        self.assertEqual(shapes[1], shapes[2])
    
    def test_get_different_shape(self):
        """Test the get_different_shape function"""
        # Get multiple different shapes
        shapes = get_different_shape(3, "LINEAR")
        
        # Check that we got the right number of shapes
        self.assertEqual(len(shapes), 3)
        
        # Note: There's a small chance that two random shapes could be the same,
        # so we don't check that they're all different
    
    def test_get_timers(self):
        """Test the get_timers function"""
        # Test with is_same=True
        same_timers = get_timers(True, 3)
        
        # Check that we got the right number of timers
        self.assertEqual(len(same_timers), 3)
        
        # Check that all timers are the same
        self.assertEqual(same_timers[0], same_timers[1])
        self.assertEqual(same_timers[1], same_timers[2])
        
        # Test with is_same=False
        different_timers = get_timers(False, 3)
        
        # Check that we got the right number of timers
        self.assertEqual(len(different_timers), 3)

if __name__ == "__main__":
    unittest.main() 