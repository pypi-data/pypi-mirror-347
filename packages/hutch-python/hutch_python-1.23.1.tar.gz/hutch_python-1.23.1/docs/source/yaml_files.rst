Yaml Files
==========

``hutch-python`` uses a ``conf.yml`` file for basic configuration. This is a
standard yaml file with the following valid keys:
``hutch``, ``db``, ``load``, ``load_level``, ``experiment``, ``obj_config``,
``daq_type``, ``daq_host``, and ``daq_platform``, ``exclude_devices``.


hutch
-----

The ``hutch`` key expects a single string, the hutch name.

.. code-block:: YAML

   hutch: xpp


This key is used to:

- pick objects to load from ``happi``
- automatically select the active experiment
- create the correct ``daq`` object
- create the ``xxx.db`` module
- display the hutch banner


db
--

The ``db`` key expects a single string, the file path.

.. code-block:: YAML

   db: /reg/g/pcds/pyps/apps/hutch-python/device_config/db.json


The file path can be either relative to the ``conf.yml`` file or absolute.
In practice, you would only change this string for development purposes.

This key is used to:

- load objects from ``happi``
- set up the ``xxx_beampath`` object


load
----

The load key expects a string or a list of strings, the modules to load.

.. code-block:: YAML

   load: xpp.beamline


.. code-block:: YAML

   load:
     - xpp.beamline
     - xpp.random_stuff


Both of these formats are valid.

This key is used to include hutch-specific code.
``hutch-python`` will attempt to do a
``from module import *`` for each of these modules.


load_level
----------
The ``load_level`` key expects one of the following strings, corresponding to the
amount of ophyd devices to load:

- ``UPSTREAM``: The hutch's devices, and devices upstream from the requested hutch.
  If there are multiple paths to the requested hutch, all paths' devices are loaded.

- ``STANDARD``: Devices gathered via ``UPSTREAM``, plus devices that share the
  "beamline" field in happi with the ``UPSTREAM`` devices.  (The current standard)

- ``ALL``: All devices in the happi database.  Use this option at your own risk.

.. code-block:: YAML

   load_level: UPSTREAM


experiment
----------

The ``experiment`` key expects a dictionary with proposal and run, both
strings. It is not needed to provide an experiment key unless you would like
to load an experiment other than the active experiment; handy for debugging.

.. code-block:: YAML

   experiment:
     proposal: ls25
     run: 16


This key is used to force the questionnaire and experiment file to be from a
particular experiment.

.. _obj_conf_yaml:


obj_conf
--------

The ``obj_conf`` key expects a single string, a file path.

.. code-block:: YAML

   obj_config: /cds/group/pcds/pyps/apps/hutch-python/xxx/tabs.yml

The file path can be either relative to the ``conf.yml`` file or absolute.
This key is used to customize objects after they have been loaded.
Currently, this supports modifying:

- attributes visible by tab-completion
- the ``kind`` of an object

on a class-wide or device-by-device basis.

For more information, see :ref:`object-configuration`.


daq_type
--------

The ``daq_type`` key is optional. If omitted, the default value is 'lcls1'
for backwards compatibility with existing hutch python setups.
This key expects a string with one of four valid values:
'lcls1', 'lcls1-sim', 'lcls2', or 'nodaq', to pick between creating an
LCLS1-style daq, a simulated LCLS1-style daq, an LCLS2-style daq,
or no daq respectively.


daq_host
--------

The daq collection host as a string. This is a required key
when using the lcls2 daq_type, and is ignored with any other daq_type.
It will be used in the creation of the lcls2 daq object.


daq_platform
------------

A dictionary description of which daq platform to use. This is used to
determine whether to use the primary or secondary elog in hutches with
two daqs, and is used to set up the lcls2 daq_type. If omitted entirely,
platform 0 and the primary elog will be used.
This dictionary has a required key, "default" that points to an integer
that is the normal platform to use, associated with the primary
experiment. Additional keys are interpreted as hostnames to use
alternate platforms for. Alternate platforms will post to the
secondary elog.


exclude_devices
------------
The ``exclude_devices`` key is optional. ``exclude_devices`` expects a string
that starts with a "-" symbol on each line. The string is the name of a device
that should not be loaded.

This feature reduces the amount of unnecessary information shown in the console
at load time. The list uses the following format:

.. code-block:: YAML

   exclude_devices:
      - crix_cryo_y
      - at2k2_calc
      - tmo_lamp_sqr1


additional_devices
------------
The ``additional_devices`` key is optional. This key allows hutch-python to
load additional devices that are on a different beamline or in a different
hutch/area. The first entry below ``additional_devices`` is a search name,
such as 'tmo_sqr1_search'. Search names are arbitrarily determined by the user
but should start with a letter or number. Each search name is followed by a
happi search key, such as "beamline" and a value. For example, "beamline: TMO".
This tells hutch-python to gather all devices on the TMO beamline and load
them. A second search criterion can be added below "beamline: TMO" to constrain
the search further, so that only those devices that fit both search criteria
will be loaded. For example, adding "device_class: pcdsdevices.sqr1.SQR1" below
"beamline: TMO" tells hutch-python to load devices from the TMO beamline whose
"device_class" key has a value of "pcdsdevices.sqr1.SQR1". More lines can be
added to obtain even more specific search results.

A search value can contain a wildcard symbol (*). For example, "name: tmo_*".

In the example below hutch-python will load all devices from "tmo_sqr1_search",
"las_search", and "crix_search".

.. code-block:: YAML

   additional_devices:
      tmo_sqr1_search:
         beamline: TMO
         device_class: pcdsdevices.sqr1.SQR1
         z: -1, 1
      las_search:
        name: LAS
      crix_search:
         name: crix_*


Full File Example
-----------------

.. code-block:: YAML

   hutch: xpp

   db: /reg/g/pcds/pyps/apps/hutch-python/device_config/db.json

   load:
     - xpp.beamline
