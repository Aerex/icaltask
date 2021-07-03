icaltask 
========

.. image:: https://img.shields.io/badge/version-0.0.1-blue.svg?cacheSeconds=2592000
   :alt: version
   :width: 100%
   :align: center

icaltask is a `taskwarrior <https://taskwarrior.org/>`_ hook that converts taskwarrior tasks into iCalendar VTODO events and exports them to an iCalendar server.  

Install
-------

Using python-setuptools
~~~~~~~~~~~~~~~~~~~~~~~
::

   $ python3 setup.py install

Configuration
-------------
Generate the sample configuration file by running the following command. How to use configure the file is documented in the file.
::

  $ icaltask copy-config

Hooks and UDA Configs
~~~~~~~~~~~~~~~~~~~~~
Run the following command to create the on-add and on-modify hooks. This will also add the necessary UDA configuration into your taskwarrior configuration file
::
  
  $ icaltask install 

To remove the hooks and UDA configuration run the following command
::

  $ icaltask uninstall

Related Projects
----------------
`baikal-storage-plugin <https://github.com/Aerex/baikal-storage-plugin>`_
