Module betterstack.uptime
==========================

This module will handle all low-level API calls, using a semi-modular approach. Whilst the API should always return its' objects
with the format below, the module does not care about what data is assigned to every object. This is generated at runtime, thus 
guaranteeing compliance with the API. This does mean that the interface to the user could change, so beware!

Standard data format
^^^^^^^^^^^^^^^^^^^^

.. highlight:: json
.. code-block:: json

   {
      "data": {
         "id": 1234,
         "attributes": {
            "somekey": "somevalue",
         }
      }
   }




Submodules
-----------

.. toctree::
    :maxdepth: 3
    :glob:
    :titlesonly:

    ./*

Module contents
---------------

.. automodule:: betterstack.uptime
   :members:
   :undoc-members:
   :show-inheritance:


