"""
Tests for the case_conversion module.
"""

import unittest
from pyutilkit.string_utils.case_conversion import to_snake_case, to_camel_case, to_pascal_case


class TestCaseConversion(unittest.TestCase):
    """
    Test case for the case_conversion module.
    """
    
    def test_to_snake_case(self):
        """Test the to_snake_case function."""
        self.assertEqual(to_snake_case("HelloWorld"), "hello_world")
        self.assertEqual(to_snake_case("helloWorld"), "hello_world")
        self.assertEqual(to_snake_case("hello-world"), "hello_world")
        self.assertEqual(to_snake_case("hello world"), "hello_world")
        self.assertEqual(to_snake_case("hello_world"), "hello_world")
        self.assertEqual(to_snake_case("HELLO_WORLD"), "hello_world")
        self.assertEqual(to_snake_case("123HelloWorld"), "123_hello_world")
        self.assertEqual(to_snake_case(""), "")
    
    def test_to_camel_case(self):
        """Test the to_camel_case function."""
        self.assertEqual(to_camel_case("hello_world"), "helloWorld")
        self.assertEqual(to_camel_case("HelloWorld"), "helloWorld")
        self.assertEqual(to_camel_case("hello-world"), "helloWorld")
        self.assertEqual(to_camel_case("hello world"), "helloWorld")
        self.assertEqual(to_camel_case("HELLO_WORLD"), "helloWorld")
        self.assertEqual(to_camel_case("123_hello_world"), "123HelloWorld")
        self.assertEqual(to_camel_case(""), "")
    
    def test_to_pascal_case(self):
        """Test the to_pascal_case function."""
        self.assertEqual(to_pascal_case("hello_world"), "HelloWorld")
        self.assertEqual(to_pascal_case("helloWorld"), "HelloWorld")
        self.assertEqual(to_pascal_case("hello-world"), "HelloWorld")
        self.assertEqual(to_pascal_case("hello world"), "HelloWorld")
        self.assertEqual(to_pascal_case("HELLO_WORLD"), "HelloWorld")
        self.assertEqual(to_pascal_case("123_hello_world"), "123HelloWorld")
        self.assertEqual(to_pascal_case(""), "")


if __name__ == "__main__":
    unittest.main() 