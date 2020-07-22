kustomization
=============

Description
-----------

A very simple wrapper around ``kubectl apply -k``.

Requirements
------------

* ``kubectl``

Parameters
----------

+---------------+---------------------------------------------------+
| **Parameter** | **Comment**                                       |
+---------------+---------------------------------------------------+
| N/A           | Module does not support additional parameters     |
+---------------+---------------------------------------------------+

Examples
--------

.. code-block:: yaml

  # This module executes "kubectl apply -k <directory>"
  - name: Deploy app
    kustomization: app/  # in Narrenschiff paths are relative to files/ dir in a course project

Status
------

.. warning::

  This module is experimental.
