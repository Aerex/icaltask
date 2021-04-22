icaltask - Synchronize between Taskwarrior and iCalendar TODO events
#####################################################################

.. image:: https://img.shields.io/badge/version-0.0.1-blue.svg?cacheSeconds=2592000
   :alt: version
   :width: 100%
   :align: center

## Install
==========
.. code-block::bash
   $ pip install icaltask

## Usage
========

Copy sample configuration 
-------------------------
.. code-block::bash
   $ icaltask copy-config

Hooks and UDA Configs
----------------
Run the following command to create the on-add and on-modify hooks. This will also add the necessary UDA configuration into your taskwarrior configuration file
.. code-block::bash
   $ icaltask install
