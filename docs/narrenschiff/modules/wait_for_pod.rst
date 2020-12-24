wait_for_pod
============

Description
-----------

Wait for a pod to be ready.

Requirements
------------

* ``kubectl``

Parameters
----------

.. list-table::
  :header-rows: 1

  * - Parameter
    - Comment
  * - namespace
    - Namespace in which the pod is located
  * - threshold_replicas
    - How many replicast should be ready in order for task to be considered completed
  * - grep_pod_name
    - Pod you are waiting

Examples
--------

.. code-block:: yaml

  - name: Wait for a pod
    wait_for_pod:
      namespace: cert-manager
      threshold_replicas: 1  # This is 1 in e.g. 1/2
      grep_pod_name: cert-manager-webhook  # not a full name, only a part

Status
------

.. warning::

  This module is experimental.
