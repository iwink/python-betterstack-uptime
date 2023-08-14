import unittest
import sys, json

if sys.version_info >= (3, 3):  # pragma: no cover
    from unittest import mock
else:  # pragma: no cover
    import mock


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