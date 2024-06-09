#!/usr/bin/python3
"""
Contains test for DBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
from models import storage
DBStorage = db_storage.DBStorage
class_instances = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to validate the documentation and style of DBstorage class"""
    @classmethod
    def setUpClass(cls):
        """Setting up for the doc tests"""
        cls.db_storage_funcs = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Ensure models/engine/db_storage.py conforms to PEP8."""
        pep8_style = pep8.StyleGuide(quiet=True)
        result = pep8_style.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8_style = pep8.StyleGuide(quiet=True)
        result = pep8_style.check_files(['tests/test_models/test_engine/test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Validates the exist_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Ensure the DBStorage class has a docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Check for the presence of docstrings in DBStorage methods"""
        for func in self.db_storage_funcs:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Validates that all returns a dictionary"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """Validate that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Check if save properly saves objects to file.json"""

    def test_get_db(self):
        """ Tests method for obtaining an instance db storage"""
        dic = {"name": "Cundinamarca"}
        instance = State(**dic)
        storage.new(instance)
        storage.save()
        get_instance = storage.get(State, instance.id)
        self.assertEqual(get_instance, instance)

    def test_count(self):
        """ Tests count method db storage """
        dic = {"name": "Vecindad"}
        state = State(**dic)
        storage.new(state)
        dic = {"name": "Mexico", "state_id": state.id}
        city = City(**dic)
        storage.new(city)
        storage.save()
        count = storage.count()
        self.assertEqual(len(storage.all()), count)
