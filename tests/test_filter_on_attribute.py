import unittest
import sys, json

if sys.version_info >= (3, 3):  # pragma: no cover
    from unittest import mock
else:  # pragma: no cover
    import mock

from betterstack.uptime.helpers import filter_on_attribute

class TestStringMethods(unittest.TestCase):
    def setUp(self):
        class TestClass():
            def __init__(self, *args, **kwargs):
                for k,v in kwargs.items():
                    print("Setting",k,v)
                    setattr(self, k, v)
        self.test_instance_1 = TestClass(test1="hello", test2="world")
        self.test_instance_2 = TestClass(test1="hello", test2="World!")
        self.test_instance_3 = TestClass(test3="Hello, World!")
        self.test_instances = [self.test_instance_1, self.test_instance_2, self.test_instance_3]
    
    def test_variable_in_object(self):
        
        attrs = filter_on_attribute(self.test_instances, "test1", "hello")

        self.assertEqual(len(attrs), 2)
        self.assertEqual(attrs[0].test1, "hello")
        self.assertEqual(attrs[0].test2, "world")
        self.assertEqual(attrs[1].test1, "hello")
        self.assertEqual(attrs[1].test2, "World!")