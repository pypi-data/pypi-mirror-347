"""
Basic tests for the PyUtilKit package.
"""

import unittest
from pyutilkit.string_utils import to_snake_case, is_palindrome
from pyutilkit.list_utils import flatten, chunk
from pyutilkit.math_utils import safe_divide, is_prime


class TestStringUtils(unittest.TestCase):
    """Test case for string_utils module."""
    
    def test_to_snake_case(self):
        """Test to_snake_case function."""
        self.assertEqual(to_snake_case("HelloWorld"), "hello_world")
        self.assertEqual(to_snake_case("helloWorld"), "hello_world")
        self.assertEqual(to_snake_case("hello-world"), "hello_world")
    
    def test_is_palindrome(self):
        """Test is_palindrome function."""
        self.assertTrue(is_palindrome("racecar"))
        self.assertTrue(is_palindrome("Race Car", ignore_spaces=True))
        self.assertFalse(is_palindrome("hello"))


class TestListUtils(unittest.TestCase):
    """Test case for list_utils module."""
    
    def test_flatten(self):
        """Test flatten function."""
        self.assertEqual(flatten([1, [2, 3], [4, [5, 6]]]), [1, 2, 3, 4, 5, 6])
        self.assertEqual(flatten([1, [2, 3], [4, [5, 6]]], depth=1), [1, 2, 3, 4, [5, 6]])
    
    def test_chunk(self):
        """Test chunk function."""
        self.assertEqual(chunk([1, 2, 3, 4, 5, 6, 7], 3), [[1, 2, 3], [4, 5, 6], [7]])
        self.assertEqual(chunk([1, 2, 3], 1), [[1], [2], [3]])


class TestMathUtils(unittest.TestCase):
    """Test case for math_utils module."""
    
    def test_safe_divide(self):
        """Test safe_divide function."""
        self.assertEqual(safe_divide(10, 2), 5.0)
        self.assertEqual(safe_divide(10, 0, default=0), 0)
    
    def test_is_prime(self):
        """Test is_prime function."""
        self.assertTrue(is_prime(2))
        self.assertTrue(is_prime(17))
        self.assertFalse(is_prime(4))
        self.assertFalse(is_prime(1))


if __name__ == "__main__":
    unittest.main() 