import unittest
import time
from clockclock24_py.utils.utils import (
    get_random_number,
    get_random_boolean,
    get_max_animation_time,
    Timeout,
    start_timeout,
    run_sequences
)

class TestUtils(unittest.TestCase):
    """Test cases for the utils module"""
    
    def test_get_random_number(self):
        """Test the get_random_number function"""
        # Test with default min_val
        for _ in range(100):
            num = get_random_number(10)
            self.assertTrue(1 <= num <= 10)
        
        # Test with custom min_val
        for _ in range(100):
            num = get_random_number(20, 5)
            self.assertTrue(5 <= num <= 20)
    
    def test_get_random_boolean(self):
        """Test the get_random_boolean function"""
        # Just ensure it returns a boolean
        for _ in range(100):
            result = get_random_boolean()
            self.assertIsInstance(result, bool)
    
    def test_get_max_animation_time(self):
        """Test the get_max_animation_time function"""
        # Create a test timer with known animation times
        timer = [
            [
                [
                    {"hours": 0, "minutes": 0, "animation_time": 100},
                    {"hours": 0, "minutes": 0, "animation_time": 200}
                ],
                [
                    {"hours": 0, "minutes": 0, "animation_time": 300},
                    {"hours": 0, "minutes": 0, "animation_time": 400}
                ]
            ],
            [
                [
                    {"hours": 0, "minutes": 0, "animation_time": 500},
                    {"hours": 0, "minutes": 0, "animation_time": 600}
                ],
                [
                    {"hours": 0, "minutes": 0, "animation_time": 700},
                    {"hours": 0, "minutes": 0}  # No animation_time
                ]
            ]
        ]
        
        # The max animation time should be 700
        self.assertEqual(get_max_animation_time(timer), 700)
    
    def test_timeout(self):
        """Test the Timeout class"""
        # Test that a timeout completes
        timeout = Timeout(100)
        completed = False
        
        def on_complete():
            nonlocal completed
            completed = True
        
        timeout.then(on_complete)
        timeout.start()
        
        # Wait for the timeout to complete
        time.sleep(0.2)
        self.assertTrue(completed)
        
        # Test cancellation
        timeout = Timeout(1000)
        cancelled = False
        
        def on_cancel():
            nonlocal cancelled
            cancelled = True
        
        timeout.catch(on_cancel)
        timeout.start()
        timeout.cancel()
        
        self.assertTrue(cancelled)
    
    def test_start_timeout(self):
        """Test the start_timeout function"""
        # Just a simple test to ensure it returns a Timeout object
        timeout = start_timeout(100)
        self.assertIsInstance(timeout, Timeout)
    
    def test_run_sequences(self):
        """Test the run_sequences function"""
        # Create a list of timeout functions
        results = []
        
        def create_timeout_func(value):
            def func():
                timeout = Timeout(50)
                timeout.then(lambda: results.append(value))
                return timeout.start()
            return func
        
        sequence_functions = [
            create_timeout_func(1),
            create_timeout_func(2),
            create_timeout_func(3)
        ]
        
        # Run the sequences
        run_sequences(sequence_functions)
        
        # Wait for all timeouts to complete
        time.sleep(0.3)
        
        # Check that the results are in order
        self.assertEqual(results, [1, 2, 3])

if __name__ == "__main__":
    unittest.main() 