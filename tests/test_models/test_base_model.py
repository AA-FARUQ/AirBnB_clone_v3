#!/usr/bin/python3
"""Test for BaseModel functionality and documentation."""
from datetime import datetime
import inspect
import models
import pep8 as pycodestyle
import time
import unittest
from unittest import mock

BaseModel = models.base_model.BaseModel
module_docstring = models.base_model.__doc__


class TestBaseModelDocumentation(unittest.TestCase):
    """Tests to verify the documentation and style of BaseModel class"""

    @classmethod
    def setUpClass(self):
        """Set up for docstring tests"""
        cls.base_model_methods = inspect.getmembers(BaseModel, inspect.isfunction)

    def test_pep8_conformance(self):
        """Check if models/base_model.py conforms to PEP8."""
        for filepath in ['models/base_model.py',
                     'tests/test_models/test_base_model.py']:
            with self.subTest(filepath=filepath):
                errors = pycodestyle.Checker(filepath).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Ensure the module docstring exists."""
        self.assertIsNot(module_docstring, None,
                         "base_model.py needs a docstring")
        self.assertTrue(len(module_docstring) > 1,
                        "base_model.py needs a docstring")

    def test_class_docstring(self):
        """Test the BaseModel class has a docstring"""
        self.assertIsNot(BaseModel.__doc__, None,
                         "BaseModel class needs a docstring")
        self.assertTrue(len(BaseModel.__doc__) >= 1,
                        "BaseModel class needs a docstring")

    def test_func_docstrings(self):
        """Ensure docstrings exist in BaseModel methods"""
        for method in self.base_model_methods:
            with self.subTest(function=func):
                self.assertIsNot(
                    method[1].__doc__,
                    None,
                    "{:s} method needs a docstring".format(method[0])
                )
                self.assertTrue(
                    len(method[1].__doc__) > 1,
                    "{:s} method needs a docstring".format(method[0])
                )


class TestBaseModel(unittest.TestCase):
    """Test the BaseModel class."""

    def test_instantiation(self):
        """Ensure objects are correctly created"""
        instance = BaseModel()
        self.assertIs(type(instance), BaseModel)
        instance.name = "Holberton"
        instance.number = 89
        attributes_types = {
            "id": str,
            "created_at": datetime,
            "updated_at": datetime,
            "name": str,
            "number": int
        }
        for attr, attr_type in attributes_types.items():
            with self.subTest(attr=attr, attr_type=attr_typ):
                self.assertIn(attr, instance.__dict__)
                self.assertIs(type(instance.__dict__[attr]), attr_type)
        self.assertEqual(instance.name, "Holberton")
        self.assertEqual(instance.number, 89)

    def test_datetime_attributes(self):
        """Check datetime objects and created_at/updated_at value."""
        start_time = datetime.now()
        instance1 = BaseModel()
        end_time = datetime.now()
        self.assertTrue(start_time <= instance1.created_at <= end_time)
        time.sleep(1e-4)
        start_time = datetime.now()
        instance2 = BaseModel()
        end_timec = datetime.now()
        self.assertTrue(start_time <= instance2.created_at <= end_time)
        self.assertEqual(instance1.created_at, instance1.updated_at)
        self.assertEqual(instance2.created_at, instance2.updated_at)
        self.assertNotEqual(instance1.created_at, instance2.created_at)
        self.assertNotEqual(instance1.updated_at, instance2.updated_at)

    def test_uuid(self):
        """Check if id is a valid UUID"""
        instance1 = BaseModel()
        instance2 = BaseModel()
        for instance in [instance1, instance2]:
            uuid = instance.id
            with self.subTest(uuid=uuid):
                self.assertIs(type(uuid), str)
                self.assertRegex(uuid,
                                 '^[0-9a-f]{8}-[0-9a-f]{4}'
                                 '-[0-9a-f]{4}-[0-9a-f]{4}'
                                 '-[0-9a-f]{12}$')
        self.assertNotEqual(instance1.id, instance2.id)

    def test_to_dict(self):
        """Convert object attributes to dictionary for JSON."""
        instance = BaseModel()
        instance.name = "Holberton"
        instance.my_number = 89
        instance_dict = instance.to_dict()
        expected_attributes = ["id",
                          "created_at",
                          "updated_at",
                          "name",
                          "my_number",
                          "__class__"]
        self.assertCountEqual(instance_dict.keys(), expected_attributes)
        self.assertEqual(instance_dict['__class__'], 'BaseModel')
        self.assertEqual(instance_dict['name'], "Holberton")
        self.assertEqual(instance_dict['my_number'], 89)

    def test_to_dict_values(self):
        """Ensure correct values in the dictionary returned from to_dict."""
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        instannce = BaseModel()
        instance_dict = instance.to_dict()
        self.assertEqual(instance_dict["__class__"], "BaseModel")
        self.assertEqual(type(instance_dict["created_at"]), str)
        self.assertEqual(type(instance_dict["updated_at"]), str)
        self.assertEqual(instance_dict["created_at"], instance.created_at.strftime(time_format))
        self.assertEqual(instance_dict["updated_at"], instance.updated_at.strftime(time_format))

    def test_str(self):
        """Check if the str method output is correct."""
        instance = BaseModel()
        expected_str = "[BaseModel] ({}) {}".format(instance.id, instance.__dict__)
        self.assertEqual(expected_expected_str, str(instance))

    @mock.patch('models.storage')
    def test_save(self, mock_storage):
        """Update 'update_at' with save method and call storage.save`"""
        instance = BaseModel()
        old_created_at = inst.created_at
        old_updated_at = inst.updated_at
        inst.save()
        new_created_at = inst.created_at
        new_updated_at = inst.updated_at
        self.assertNotEqual(old_updated_at, new_updated_at)
        self.assertEqual(old_created_at, new_created_at)
        self.assertTrue(mock_storage.new.called)
        self.assertTrue(mock_storage.save.called)
