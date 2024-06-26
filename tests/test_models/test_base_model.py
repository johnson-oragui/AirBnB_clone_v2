#!/usr/bin/python3
"""
Unit tests for the BaseModel class.
"""

from models.base_model import BaseModel, Base
import unittest
import datetime
import json
import os

STORAGE_TYPE = os.getenv('HBNB_TYPE_STORAGE')


class Test_Basemodel(unittest.TestCase):
    """
    Test class for the BaseModel model.
    """
    @classmethod
    def setUpClass(cls):
        """Set up any necessary resources for the test cases."""
        try:
            os.rename('file.json', 'tmp.json')
            cls.name = 'BaseModel'
            cls.value = BaseModel
        except Exception:
            pass

    @classmethod
    def tearDownClass(cls):
        """Clean up any resources created during the test cases."""
        try:
            os.rename('tmp.json', 'file.json')
            del cls.name
            del cls.value
        except Exception:
            pass

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing DBStorage')
    def test_default(self):
        """Test case to check if an instance of \
                BaseModel is created properly."""
        base_instance = self.value()
        self.assertEqual(type(base_instance), self.value)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing DBStorage')
    def test_kwargs(self):
        """
        Test case to check if an instance of BaseModel\
                can be created with keyword arguments.
        """
        base_instance = self.value()
        copy = base_instance.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is base_instance)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing DBStorage')
    def test_kwargs_int(self):
        """
        Test case to check if TypeError is raised when\
                creating BaseModel instance with integer keys.
        """
        base_instance = self.value()
        copy = base_instance.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing DBStorage')
    def test_save(self):
        """Test case to check if the 'save' method saves \
                the BaseModel instance properly."""
        base_instance = self.value()
        base_instance.save()
        key = self.name + "." + base_instance.id
        with open('file.json', 'r') as f:
            objs = json.load(f)
            self.assertEqual(objs[key], base_instance.to_dict())

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing DBStorage')
    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     'Testing DBStorage')
    def test_str(self):
        """Test case to check if the 'str' method returns\
                the expected string representation."""
        base_instance = self.value()
        self.assertEqual(str(base_instance),
                         '[{}] ({}) {}'.format(self.name,
                                               base_instance.id,
                                               base_instance.__dict__))

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing DBStorage')
    def test_todict(self):
        """Test case to check if the 'to_dict' method
                returns a dictionary representation of
                the BaseModel instance.
        """
        base_instance = self.value()
        n = base_instance.to_dict()
        self.assertEqual(base_instance.to_dict(), n)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing DBStorage')
    def test_kwargs_none(self):
        """Test case to check if TypeError is raised\
                when creating BaseModel instance with None keys."""
        none_dict = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**none_dict)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing DBStorage')
    def test_id(self):
        """Test case to check the data type of the 'id' attribute."""
        base_instance = self.value()
        self.assertEqual(type(base_instance.id), str)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing DBStorage')
    def test_created_at(self):
        """Test case to check the data\
                type of the 'created_at' attribute."""
        base_instance = self.value()
        self.assertEqual(type(base_instance.created_at), datetime.datetime)

    @unittest.skipIf(STORAGE_TYPE != 'db', 'Testing FileStorage')
    def test_mapped_to_base(self):
        """
        test if basemodel is mapped to sqlalchemy
        """
        b_instance = BaseModel()
        self.assertFalse('_sa_instance_state' in b_instance.__dict__)

    @unittest.skipIf(STORAGE_TYPE != 'db', 'Testing FileStorage')
    def test_is_subclass(self):
        """
        test if basemodel is mapped to sqlalchemy
        """
        b_instance = BaseModel()
        self.assertFalse(isinstance(b_instance, Base))


if __name__ == "__main__":
    unittest.main()
