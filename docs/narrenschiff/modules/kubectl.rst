kubectl
=======

Description
-----------

Execute ``kubectl`` commands. Interact with your Kubernetes cluster.

Requirements
------------

* ``kubectl``

Parameters
----------

+---------------+-------------------------------------------------------------------------------------------------------------------------------------------------+
| **Parameter** | **Comment**                                                                                                                                     |
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------------+
| command       | Any kubectl command with nested subcommands                                                                                                     |
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------------+
| args          | flag/value pairs, a flag needs to be listed by its full name (e.g. you can't use ``f`` for ``-f/--filename``, you have to use ``filename``)     |
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------------+

Examples
--------

.. code-block:: yaml

  # Both get (command) and namespaces (subcommand) are inputs for parameter "command"
  # kubectl get namespaces
  - name: List all namespaces
    kubectl:
      command: get namespaces

  # "args" paramater taks only flag/value pairs
  # kubectl get pods --namespaces default
  - name: List all pods in default namespace
    kubectl:
      command: get pods
      args:
        namespace: default

  # If you need to create a namespace you can just put a whole command in "command" paramater
  # kubectl create namespace cert-manager
  - name: Create namespace for cert-manager
    kubectl:
      command: create namespace cert-manager

  # Value of a flag depends on underlying input kubectl is expecting
  # kubectl apply -f project/files/secretmap.yaml,project/files/configmap.yaml,project/files/deployment.yaml --namespace development
  - name: Deploy application
    kubectl:
    command: apply
    args:
      filename:
        - secretmap.yaml  # in Narrenschiff paths are relative to files/ dir in a course project
        - configmap.yaml
        - deployment.yaml
      namespace: development

  # If you have a single file that you have to pass to -f, you can also use this syntax
  # kubectl apply -f project/files/configmap.yaml
  - name: Deploy config map
    kubectl:
      command: apply
      args:
        filename: configmap.yaml

  # You can also apply configurations from URLs
  # kubectl apply -f https://raw.githubusercontent.com/jetstack/cert-manager/release-0.8/deploy/manifests/00-crds.yaml --namespace cert-manager
  - name: Install cert-manager
    kubectl:
      command: apply
      args:
        filename:
          - https://raw.githubusercontent.com/jetstack/cert-manager/release-0.8/deploy/manifests/00-crds.yaml
        namespace: cert-manager

  # You can mix URLs with file paths
  - name: Deploy applications
    kubectl:
    command: apply
    args:
      filename:
        - secretmap.yaml
        - configmap.yaml
        - deployment.yaml
        - https://raw.githubusercontent.com/kubernetes/kubectl/master/testdata/apply/deploy-clientside.yaml
      namespace: development

Status
------

.. warning::

  This module is experimental.
