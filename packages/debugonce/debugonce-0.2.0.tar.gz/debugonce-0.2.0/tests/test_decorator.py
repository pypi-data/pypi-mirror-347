# tests/test_decorator.py
import unittest
from debugonce_packages.decorator import debugonce
import json
import os

class TestDebugOnceDecorator(unittest.TestCase):
    def test_capture_state(self):
        # Test capturing state with no exception
        @debugonce
        def add(a, b):
            return a + b

        result = add(2, 3)
        self.assertEqual(result, 5)

        # Check if the state is saved to a file
        self.assertTrue(os.path.exists("debugonce.json"))

        # Load the state from the file
        with open("debugonce.json", "r") as f:
            state = json.load(f)

        # Check if the state is correct
        self.assertEqual(state["function"], "add")
        self.assertEqual(state["args"], [2, 3])  # Expect a list instead of a tuple
        self.assertEqual(state["kwargs"], {})
        self.assertEqual(state["result"], 5)
        self.assertIsNone(state["exception"])

    def test_capture_state_with_exception(self):
        # Test capturing state with exception
        @debugonce
        def divide(a, b):
            return a / b

        with self.assertRaises(ZeroDivisionError):
            divide(2, 0)

        # Check if the state is saved to a file
        self.assertTrue(os.path.exists("debugonce.json"))

        # Load the state from the file
        with open("debugonce.json", "r") as f:
            state = json.load(f)

        # Check if the state is correct
        self.assertEqual(state["function"], "divide")
        self.assertEqual(state["args"], [2, 0])  # Expect a list instead of a tuple
        self.assertEqual(state["kwargs"], {})
        self.assertIsNone(state["result"])
        self.assertIsInstance(state["exception"], str)

if __name__ == "__main__":
    unittest.main()