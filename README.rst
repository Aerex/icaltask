icaltask 
========

.. image:: https://img.shields.io/badge/version-0.0.1-blue.svg?cacheSeconds=2592000
   :alt: version
   :width: 100%
   :align: center

icaltask is a Taskwarrior hook that  

Install
-------
::

   $ python3 setup.py install

Configuration
-------------

Hooks and UDA Configs
~~~~~~~~~~~~~~~~~~~~~
Run the following command to create the on-add and on-modify hooks. This will also add the necessary UDA configuration into your taskwarrior configuration file
::
  
  $ icaltask install 

To remove the hooks and UDA configuration run the following command
 
::
  $ icaltask uninstall
