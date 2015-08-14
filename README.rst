Hygieia TeamCity
================

A TeamCity collector for Hygieia.

Usage
=====

Create a dashboard ``anonweb_py27`` for app ``anonweb`` and load builds from
TeamCity's job ``Anonweb_2_Branches_Py27``. If the dashboard doesn't exist,
it will be created automatically.

.. code-block::

    hytc sync anonweb anonweb_py27 --builds=Anonweb_2_Branches_Py27
