import unittest
import sys

if sys.version_info >= (3, 3):  # pragma: no cover
    from unittest import mock
else:  # pragma: no cover
    import mock  # noqa: F401

from betterstack.uptime.mixins import DynamicVariableMixin


class DynamicVariableMixinTests(unittest.TestCase):

    def test_modified_variable(self):
        test_instance = DynamicVariableMixin()
        test_instance.reset_variable_tracking()
        self.assertEqual(len(test_instance.get_modified_properties()), 0)
        test_instance.add_tracked_property("hello", "world")
        self.assertEqual(test_instance.hello, "world")
        self.assertTrue("hello" not in test_instance.get_modified_properties())
        test_instance.hello = "world"
        self.assertTrue("hello" not in test_instance.get_modified_properties())
        test_instance.hello = "World!"
        self.assertTrue("hello" in test_instance.get_modified_properties())

    def test_modified_variable_update(self):
        # Make sure variable is there before setting
        test_instance = DynamicVariableMixin()
        test_instance.reset_variable_tracking()
        test_instance.add_tracked_property("hello", "World!")
        test_instance.hello = "World"
        self.assertEqual(test_instance.hello, "World")
        self.assertEqual(test_instance.get_modified_properties(), ['hello'])

    def test_modified_variable_noupdate(self):
        test_instance = DynamicVariableMixin()
        test_instance.reset_variable_tracking()
        test_instance.add_tracked_property("hello", "World!")
        self.assertEqual(test_instance.hello, "World!")
        self.assertEqual(test_instance.get_modified_properties(), [])

    def test_multiple_variables(self):
        test_instance_1 = DynamicVariableMixin()
        test_instance_2 = DynamicVariableMixin()
        test_instance_1.add_tracked_property('hello', "World 1")
        self.assertEqual(test_instance_1.hello, "World 1")
        test_instance_2.add_tracked_property('hello', "World 2")
        self.assertEqual(test_instance_1.hello, "World 1")
        self.assertEqual(test_instance_2.hello, "World 2")
        self.assertEqual(test_instance_1.get_modified_properties(), [])
        self.assertEqual(test_instance_2.get_modified_properties(), [])
        test_instance_1.hello = "Modified"
        self.assertEqual(test_instance_1.hello, "Modified")
        self.assertEqual(test_instance_2.hello, "World 2")
        self.assertEqual(test_instance_1.get_modified_properties(), ['hello'])
        self.assertEqual(test_instance_2.get_modified_properties(), [])
