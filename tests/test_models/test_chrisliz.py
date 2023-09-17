#!/usr/bin/python3

import unittest
import io
import sys
from unittest.mock import patch

def print_name():
    name = "Chrris Liz"
    print(f"My name is {name}")

class TestPrintName(unittest.TestCase):

    @patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout(self, expected_output, mock_stdout):
        print_name()
        self.assertEqual(mock_stdout.getvalue().strip(), expected_output)

    def test_print_name(self):
        expected_output = "My name is Chrris Liz"
        self.assert_stdout(expected_output)

if __name__ == "__main__":
    unittest.main()
