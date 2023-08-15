Module betterstack.uptime.mixins
================================

This module contains the magic that is the `DynamicVariableMixin` class. When using this mixin, you can assign variables that track
if they get changed, whilst keeping the interface for the user the same. For example:

.. highlight:: python
.. code-block:: python

   test = DynamicVariableMixin()
   test.add_tracked_property("y", 123)
   print(test.y)
   test.y = 456
   print(test.y)
   print(test.get_modified_properties())


Module contents
---------------

.. automodule:: betterstack.uptime.mixins
   :members:
   :undoc-members:
   :show-inheritance:
