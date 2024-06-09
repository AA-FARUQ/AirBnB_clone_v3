#!/usr/bin/python3
"""
Contains the class TestConsoleDocumentation
"""

import console
import inspect
import pep8
import unittest
HBNBCommand = console.HBNBCommand


class TestConsoleDocumentation(unittest.TestCase):
    """Class for testing documentation of the console"""
    def test_pycodestyle_conformance_console(self):
        """Test that console.py follows PEP8 guidlines."""
        style_guide = pycodestyle.StyleGuide(quiet=True)
        result = style_guide.check_files(['console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pycodestyle_conformance_test_console(self):
        """Test that tests/test_console.py follows PEP8 guidlines."""
        style_guide = pycodestyle.StyleGuide(quiet=True)
        result = style_guide.check_files(['tests/test_console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_console_module_docstring(self):
        """Test for the console.py module docstring"""
        self.assertIsNot(console.__doc__, None,
                         "console.py needs a docstring")
        self.assertTrue(len(console.__doc__) >= 1,
                        "console.py needs a docstring")

    def test_HBNBCommand_class_docstring(self):
        """Test for the HBNBCommand class docstring"""
        self.assertIsNot(HBNBCommand.__doc__, None,
                         "HBNBCommand class needs a docstring")
        self.assertTrue(len(HBNBCommand.__doc__) >= 1,
                        "HBNBCommand class needs a docstring")