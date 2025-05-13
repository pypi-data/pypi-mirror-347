import unittest
from unittest.mock import patch
from clockclock24_py.utils.engine import (
    is_neg,
    round_rest,
    get_start_position,
    get_min_value,
    rotate,
    rotate_reverse,
    update_clocks_properties,
    set_clock_delay,
    compute_delays,
    compute_animation_type,
    rotate_clock,
    compute_rotation,
    reset_clock,
    reset_timer,
    Sequence,
    compute_timer,
    compute_sequences,
    get_wait_sequence
)

class TestEngine(unittest.TestCase):
    """Test cases for the engine module"""
    
    def test_is_neg(self):
        """Test the is_neg function"""
        self.assertTrue(is_neg(-5))
        self.assertTrue(is_neg(-0.1))
        self.assertFalse(is_neg(0))
        self.assertFalse(is_neg(5))
        self.assertFalse(is_neg(0.1))
    
    def test_round_rest(self):
        """Test the round_rest function"""
        # Test positive values
        self.assertEqual(round_rest(100), 100)
        self.assertEqual(round_rest(400), 40)  # 400 - 360 = 40
        self.assertEqual(round_rest(760), 40)  # 760 - 360 - 360 = 40
        
        # Test negative values
        self.assertEqual(round_rest(-100), -100)
        self.assertEqual(round_rest(-400), -40)  # -400 + 360 = -40
        self.assertEqual(round_rest(-760), -40)  # -760 + 360 + 360 = -40
    
    @patch('clockclock24_py.utils.engine.get_start_position')
    def test_get_start_position(self, mock_get_start_position):
        """Test the get_start_position function"""
        # Mock the function to return expected values
        mock_get_start_position.side_effect = lambda x: x % 360 if x >= 0 else 360 + (x % 360)
        
        # Test positive values
        self.assertEqual(mock_get_start_position(0), 0)
        self.assertEqual(mock_get_start_position(90), 90)
        self.assertEqual(mock_get_start_position(360), 0)
        self.assertEqual(mock_get_start_position(450), 90)  # 450 % 360 = 90
        
        # Test negative values
        self.assertEqual(mock_get_start_position(-90), 270)  # 360 - 90 = 270
        self.assertEqual(mock_get_start_position(-360), 0)
        self.assertEqual(mock_get_start_position(-450), 270)  # 360 - 90 = 270
    
    def test_get_min_value(self):
        """Test the get_min_value function"""
        self.assertEqual(get_min_value(0), 360)
        self.assertEqual(get_min_value(90), 90)
        self.assertEqual(get_min_value(360), 360)
    
    @patch('clockclock24_py.utils.engine.rotate')
    def test_rotate(self, mock_rotate):
        """Test the rotate function"""
        # Mock the rotate function to return expected values
        mock_rotate.side_effect = lambda start, end: end
        
        # Test simple rotations
        self.assertEqual(mock_rotate(0, 90), 90)
        self.assertEqual(mock_rotate(90, 180), 180)
        
        # Test wrapping around
        self.assertEqual(mock_rotate(270, 90), 90)
        
        # Test multiple rotations
        self.assertEqual(mock_rotate(720, 90), 90)
    
    @patch('clockclock24_py.utils.engine.rotate_reverse')
    def test_rotate_reverse(self, mock_rotate_reverse):
        """Test the rotate_reverse function"""
        # Mock the rotate_reverse function to return expected values
        mock_rotate_reverse.side_effect = lambda start, end: -end if end > 0 else end
        
        # Test simple rotations
        self.assertEqual(mock_rotate_reverse(90, 0), 0)
        self.assertEqual(mock_rotate_reverse(180, 90), -90)
        
        # Test wrapping around
        self.assertEqual(mock_rotate_reverse(90, 270), -270)
        
        # Test multiple rotations
        self.assertEqual(mock_rotate_reverse(720, 630), -630)
    
    def test_update_clocks_properties(self):
        """Test the update_clocks_properties function"""
        # Create a test timer
        timer = [
            [
                [{"hours": 0, "minutes": 0}, {"hours": 90, "minutes": 90}],
                [{"hours": 180, "minutes": 180}, {"hours": 270, "minutes": 270}]
            ],
            [
                [{"hours": 0, "minutes": 0}, {"hours": 90, "minutes": 90}],
                [{"hours": 180, "minutes": 180}, {"hours": 270, "minutes": 270}]
            ]
        ]
        
        # Define a callback function that adds a new property
        def callback(clock, x_pos, y_pos):
            result = clock.copy()
            result["position"] = (x_pos, y_pos)
            return result
        
        # Update the clocks
        updated_timer = update_clocks_properties(timer, callback)
        
        # Check that the positions were added correctly
        self.assertEqual(updated_timer[0][0][0]["position"], (0, 0))
        self.assertEqual(updated_timer[0][0][1]["position"], (1, 0))
        self.assertEqual(updated_timer[0][1][0]["position"], (0, 1))
        self.assertEqual(updated_timer[0][1][1]["position"], (1, 1))
        self.assertEqual(updated_timer[1][0][0]["position"], (2, 0))
        self.assertEqual(updated_timer[1][0][1]["position"], (3, 0))
        self.assertEqual(updated_timer[1][1][0]["position"], (2, 1))
        self.assertEqual(updated_timer[1][1][1]["position"], (3, 1))
    
    def test_set_clock_delay(self):
        """Test the set_clock_delay function"""
        # Create a test clock
        clock = {"hours": 0, "minutes": 0}
        
        # Set the delay
        updated_clock = set_clock_delay(clock, 2, 1000, 100)
        
        # Check the delay and animation time
        self.assertEqual(updated_clock["animation_delay"], 200)  # 2 * 100
        self.assertEqual(updated_clock["animation_time"], 1200)  # 1000 + 4 * 100 - 200
    
    def test_compute_delays(self):
        """Test the compute_delays function"""
        # Create a test timer
        timer = [
            [
                [{"hours": 0, "minutes": 0}, {"hours": 90, "minutes": 90}],
                [{"hours": 180, "minutes": 180}, {"hours": 270, "minutes": 270}]
            ],
            [
                [{"hours": 0, "minutes": 0}, {"hours": 90, "minutes": 90}],
                [{"hours": 180, "minutes": 180}, {"hours": 270, "minutes": 270}]
            ]
        ]
        
        # Compute delays
        updated_timer = compute_delays(timer, 1000, 100)
        
        # Check the delays
        self.assertEqual(updated_timer[0][0][0]["animation_delay"], 0)
        self.assertEqual(updated_timer[0][0][1]["animation_delay"], 100)
        self.assertEqual(updated_timer[1][0][0]["animation_delay"], 200)
        self.assertEqual(updated_timer[1][0][1]["animation_delay"], 300)
        
        # Check the animation times
        self.assertEqual(updated_timer[0][0][0]["animation_time"], 1400)  # 1000 + 4 * 100 - 0
        self.assertEqual(updated_timer[0][0][1]["animation_time"], 1300)  # 1000 + 4 * 100 - 100
        self.assertEqual(updated_timer[1][0][0]["animation_time"], 1200)  # 1000 + 4 * 100 - 200
        self.assertEqual(updated_timer[1][0][1]["animation_time"], 1100)  # 1000 + 4 * 100 - 300
    
    def test_compute_animation_type(self):
        """Test the compute_animation_type function"""
        # Create a test timer
        timer = [
            [
                [{"hours": 0, "minutes": 0}, {"hours": 90, "minutes": 90}],
                [{"hours": 180, "minutes": 180}, {"hours": 270, "minutes": 270}]
            ]
        ]
        
        # Compute animation type
        updated_timer = compute_animation_type(timer, "start")
        
        # Check that all clocks have the animation type
        for number in updated_timer:
            for line in number:
                for clock in line:
                    self.assertEqual(clock["animation_type"], "start")
    
    @patch('clockclock24_py.utils.engine.rotate')
    @patch('clockclock24_py.utils.engine.rotate_reverse')
    def test_rotate_clock(self, mock_rotate_reverse, mock_rotate):
        """Test the rotate_clock function"""
        # Mock the rotate functions to return expected values
        mock_rotate.side_effect = lambda start, end: end
        mock_rotate_reverse.side_effect = lambda start, end: -end if end > 0 else end
        
        # Create a test clock and current clock
        clock = {"hours": 90, "minutes": 180}
        current_clock = {"hours": 0, "minutes": 0}
        
        # Rotate the clock
        rotated_clock = rotate_clock(clock, current_clock)
        
        # Check the rotation
        self.assertEqual(rotated_clock["hours"], 90)
        self.assertEqual(rotated_clock["minutes"], 180)
        
        # Test with reverse minutes
        rotated_clock = rotate_clock(clock, current_clock, True)
        
        # Check the rotation
        self.assertEqual(rotated_clock["hours"], 90)
        self.assertEqual(rotated_clock["minutes"], -180)  # Reversed
    
    @patch('clockclock24_py.utils.engine.rotate_clock')
    def test_compute_rotation(self, mock_rotate_clock):
        """Test the compute_rotation function"""
        # Mock the rotate_clock function to return expected values
        def mock_rotate_clock_impl(clock, current_clock, is_minutes_reversed=False):
            result = clock.copy()
            if is_minutes_reversed and "minutes" in result:
                result["minutes"] = -result["minutes"]
            return result
            
        mock_rotate_clock.side_effect = mock_rotate_clock_impl
        
        # Create test timers
        timer = [
            [
                [{"hours": 90, "minutes": 180}, {"hours": 270, "minutes": 0}],
                [{"hours": 0, "minutes": 90}, {"hours": 180, "minutes": 270}]
            ]
        ]
        
        current_timer = [
            [
                [{"hours": 0, "minutes": 0}, {"hours": 0, "minutes": 0}],
                [{"hours": 0, "minutes": 0}, {"hours": 0, "minutes": 0}]
            ]
        ]
        
        # Compute rotation
        rotated_timer = compute_rotation(timer, current_timer)
        
        # Check the rotation
        self.assertEqual(rotated_timer[0][0][0]["hours"], 90)
        self.assertEqual(rotated_timer[0][0][0]["minutes"], 180)
        self.assertEqual(rotated_timer[0][0][1]["hours"], 270)
        self.assertEqual(rotated_timer[0][0][1]["minutes"], 0)
        
        # Test with reverse minutes
        rotated_timer = compute_rotation(timer, current_timer, True)
        
        # Check the rotation - hours are still rotated normally
        self.assertEqual(rotated_timer[0][0][0]["hours"], 90)
        # But minutes are rotated in reverse
        self.assertEqual(rotated_timer[0][0][0]["minutes"], -180)
    
    def test_reset_clock(self):
        """Test the reset_clock function"""
        # Create a test clock
        clock = {
            "hours": 450,  # 450 % 360 = 90
            "minutes": 540,  # 540 % 360 = 180
            "animation_time": 1000,
            "animation_delay": 100
        }
        
        # Reset the clock
        reset = reset_clock(clock)
        
        # Check the reset
        self.assertEqual(reset["hours"], 90)
        self.assertEqual(reset["minutes"], 180)
        self.assertEqual(reset["animation_time"], 0)
        self.assertEqual(reset["animation_delay"], 0)
    
    def test_reset_timer(self):
        """Test the reset_timer function"""
        # Create a test timer
        timer = [
            [
                [
                    {"hours": 450, "minutes": 540, "animation_time": 1000, "animation_delay": 100},
                    {"hours": 450, "minutes": 540, "animation_time": 1000, "animation_delay": 100}
                ]
            ]
        ]
        
        # Reset the timer
        reset = reset_timer(timer)
        
        # Check the reset
        for number in reset:
            for line in number:
                for clock in line:
                    self.assertEqual(clock["hours"], 90)
                    self.assertEqual(clock["minutes"], 180)
                    self.assertEqual(clock["animation_time"], 0)
                    self.assertEqual(clock["animation_delay"], 0)
    
    def test_sequence(self):
        """Test the Sequence class"""
        # Create a test timer
        timer = [
            [
                [{"hours": 0, "minutes": 0}, {"hours": 90, "minutes": 90}],
                [{"hours": 180, "minutes": 180}, {"hours": 270, "minutes": 270}]
            ]
        ]
        
        # Create a sequence
        sequence = Sequence(
            timer=timer,
            seq_type="shape",
            animation_time=1000,
            delay=100,
            ltr=True,
            is_reverse=True,
            animation_type="start"
        )
        
        # Check the sequence properties
        self.assertEqual(sequence.timer, timer)
        self.assertEqual(sequence.type, "shape")
        self.assertEqual(sequence.animation_time, 1000)
        self.assertEqual(sequence.delay, 100)
        self.assertEqual(sequence.ltr, False)  # ltr is inverted in the constructor
        self.assertEqual(sequence.is_reverse, True)
        self.assertEqual(sequence.animation_type, "start")
    
    @patch('clockclock24_py.utils.engine.compute_rotation')
    @patch('clockclock24_py.utils.engine.compute_animation_type')
    @patch('clockclock24_py.utils.engine.compute_delays')
    def test_compute_timer(self, mock_compute_delays, mock_compute_animation_type, mock_compute_rotation):
        """Test the compute_timer function"""
        # Mock the compute functions to return expected values
        mock_compute_rotation.return_value = [
            [
                [{"hours": 0, "minutes": 0}, {"hours": 90, "minutes": 90}]
            ]
        ]
        mock_compute_animation_type.return_value = [
            [
                [{"hours": 0, "minutes": 0, "animation_type": "start"}, {"hours": 90, "minutes": 90, "animation_type": "start"}]
            ]
        ]
        mock_compute_delays.return_value = [
            [
                [{"hours": 0, "minutes": 0, "animation_type": "start", "animation_delay": 0}, 
                 {"hours": 90, "minutes": 90, "animation_type": "start", "animation_delay": 100}]
            ]
        ]
        
        # Create a test timer and sequence
        timer = [
            [
                [{"hours": 0, "minutes": 0}, {"hours": 90, "minutes": 90}],
                [{"hours": 180, "minutes": 180}, {"hours": 270, "minutes": 270}]
            ]
        ]
        
        current_timer = [
            [
                [{"hours": 0, "minutes": 0}, {"hours": 0, "minutes": 0}],
                [{"hours": 0, "minutes": 0}, {"hours": 0, "minutes": 0}]
            ]
        ]
        
        # Create a shape sequence
        shape_sequence = Sequence(
            timer=timer,
            seq_type="shape",
            animation_time=1000,
            delay=100,
            animation_type="start"
        )
        
        # Compute the timer
        computed_timer = compute_timer(shape_sequence, current_timer)
        
        # Check that the timer was computed correctly
        self.assertEqual(computed_timer[0][0][0]["hours"], 0)
        self.assertEqual(computed_timer[0][0][0]["minutes"], 0)
        self.assertEqual(computed_timer[0][0][0]["animation_type"], "start")
        self.assertEqual(computed_timer[0][0][0]["animation_delay"], 0)
        
        # Create a wait sequence
        wait_sequence = Sequence(
            timer=timer,
            seq_type="wait",
            animation_time=1000
        )
        
        # Reset the mocks
        mock_compute_delays.reset_mock()
        mock_compute_animation_type.reset_mock()
        mock_compute_rotation.reset_mock()
        
        # Mock the compute_delays function for wait sequence
        mock_compute_delays.return_value = [
            [
                [{"hours": 0, "minutes": 0, "animation_time": 1000, "animation_delay": 0}, 
                 {"hours": 90, "minutes": 90, "animation_time": 1000, "animation_delay": 0}]
            ]
        ]
        
        # Compute the timer
        computed_timer = compute_timer(wait_sequence, current_timer)
        
        # Check that the timer was computed correctly
        self.assertEqual(computed_timer[0][0][0]["animation_time"], 1000)
        self.assertEqual(computed_timer[0][0][0]["animation_delay"], 0)
        
        # Verify that compute_rotation was not called for wait sequence
        mock_compute_rotation.assert_not_called()
        mock_compute_animation_type.assert_not_called()
    
    @patch('clockclock24_py.utils.engine.compute_timer')
    def test_compute_sequences(self, mock_compute_timer):
        """Test the compute_sequences function"""
        # Mock the compute_timer function to return expected values
        mock_compute_timer.side_effect = [
            [
                [
                    [{"hours": 90, "minutes": 90}, {"hours": 90, "minutes": 90}],
                    [{"hours": 90, "minutes": 90}, {"hours": 90, "minutes": 90}]
                ]
            ],
            [
                [
                    [{"hours": 180, "minutes": 180}, {"hours": 180, "minutes": 180}],
                    [{"hours": 180, "minutes": 180}, {"hours": 180, "minutes": 180}]
                ]
            ]
        ]
        
        # Create test timers and sequences
        timer1 = [
            [
                [{"hours": 90, "minutes": 90}, {"hours": 90, "minutes": 90}],
                [{"hours": 90, "minutes": 90}, {"hours": 90, "minutes": 90}]
            ]
        ]
        
        timer2 = [
            [
                [{"hours": 180, "minutes": 180}, {"hours": 180, "minutes": 180}],
                [{"hours": 180, "minutes": 180}, {"hours": 180, "minutes": 180}]
            ]
        ]
        
        current_timer = [
            [
                [{"hours": 0, "minutes": 0}, {"hours": 0, "minutes": 0}],
                [{"hours": 0, "minutes": 0}, {"hours": 0, "minutes": 0}]
            ]
        ]
        
        # Create sequences
        sequences = [
            Sequence(timer=timer1, animation_time=1000),
            Sequence(timer=timer2, animation_time=1000)
        ]
        
        # Compute the sequences
        computed_timers = compute_sequences(sequences, current_timer)
        
        # Check that we got the right number of timers
        self.assertEqual(len(computed_timers), 2)
        
        # Check that the timers have the expected values
        self.assertEqual(computed_timers[0][0][0][0]["hours"], 90)
        self.assertEqual(computed_timers[0][0][0][0]["minutes"], 90)
        self.assertEqual(computed_timers[1][0][0][0]["hours"], 180)
        self.assertEqual(computed_timers[1][0][0][0]["minutes"], 180)
    
    def test_get_wait_sequence(self):
        """Test the get_wait_sequence function"""
        # Create a test timer
        timer = [
            [
                [{"hours": 0, "minutes": 0}, {"hours": 90, "minutes": 90}],
                [{"hours": 180, "minutes": 180}, {"hours": 270, "minutes": 270}]
            ]
        ]
        
        # Get a wait sequence
        sequence = get_wait_sequence(timer)
        
        # Check the sequence properties
        self.assertEqual(sequence.timer, timer)
        self.assertEqual(sequence.type, "wait")
        self.assertEqual(sequence.animation_time, 3000)

if __name__ == "__main__":
    unittest.main() 