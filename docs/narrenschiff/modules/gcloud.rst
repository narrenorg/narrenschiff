gcloud
======

Description
-----------

Execute ``gcloud`` commands. Manage GKE.

Execution of the module will fail for the commands that require user input. Use ``--quiet`` instead. See gcloud docs_ for more info.

Requirements
------------

* ``gcloud``

Parameters
----------

.. list-table::
  :header-rows: 1

  * - Parameter
    - Comment
  * - command
    - Any gcloud command with nested subcommands
  * - args
    - flag/value pairs, a flag needs to be listed by its full name
  * - opts
    - flags without arguments i.e. switches

Examples
--------

.. code-block:: yaml

  # gcloud container clusters create test-cluster --enable-ip-alias --quiet --num-nodes 1 --machine-type n1-standard-2 --zone europe-west1-a
  - name: Create the cluster
    gcloud:
      command: "container clusters create test-cluster"
      args:
        num-nodes: 1
        machine-type: n1-standard-2
        zone: europe-west1-a
      opts:
        - enable-ip-alias  # opts are always listed as a YAML list
        - quiet

  # If you do not need any flags or switches you can place everything under the "command"
  - name: Get credentials for the cluster
    gcloud:
      command: "container clusters get-credentials test-cluster"

  - name: Enable Kubernetes API
    gcloud:
      command: "services enable container.googleapis.com"

Status
------

.. warning::

  This module is experimental.


.. _docs: https://cloud.google.com/sdk/gcloud/reference/
