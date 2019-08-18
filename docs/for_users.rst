Manual for Users
================

``narrenschiff`` is a Ansible-like configuration management tool for Kubernetes. It is advanced *wrapper* around ``kubectl``.


Requirements
------------

* Python 3.6 or higher
* ``kubectl`` v1.15 or higher

Installation
------------

At the moment it can be only built from the source code.

Primer on ``narrenschiff``
--------------------------

Basic unit of ``narrenschiff`` is ``course`` or ``courses`` i.e. file or files storing task that are to performed in sequential order. ``course`` is YAML file e.g.:

.. code-block:: yaml

  - name: Deploy config map
    kubectl:
      command: apply
      args:
        filename: "{{ files_path }}/configmap.yaml"

  - name: Apply namespaces and RBAC settings
    kubectl:
      command: apply
      args:
        filename:
          - examples/files/namespaces.yaml
          - examples/files/rbac.yaml

Each YAML file in the project is treated as a template file i.e. each ``course`` can have template variables. Template language that is powering ``courses`` is Jinja2_.

The basic directory layout of the should resemble something like this::

  project/
  ├── files  <-- Templates for you manifest files
  │   ├── namespaces.yaml
  │   ├── rbac.yaml
  │   └── app
  │       ├── kustomization.yaml
  │       ├── configmap.yaml
  │       ├── secret.yaml
  │       └── deployment.yml
  ├── tasks.yaml  <-- course file describing the deployment process
  ├── vars  <-- directory with arbitrary nesting may be used instead of vars.yaml
  │   ├── common.yaml
  │   ├── domains.yaml
  │   └── apps
  │       └── prod.yml
  ├── chest <-- directory with arbitrary nesting may be used instead of chest.yaml
  │   ├── database.yaml
  │   └── secrets.yaml
  ├── vars.yaml  <-- non encrypted variables
  └── chest.yaml  <-- encrypted variables

``files/`` directory is a directory reserved for your Kubernetes manifest files. With ``narrenschiff`` you can use Jinja2 templating language to inject variables into the manifests.

You can use ``vars.yaml`` and ``chest.yaml`` to define variables for you project. ``vars.yaml`` file or ``vars/`` directory contain unencrypted variables. ``chest.yaml`` file or ``chest/`` directory is a place to stash your *treasure* (i.e. keys, secrets, passwords, etc.). Both ``vars/`` and ``chest/`` directories can have arbitrary nesting and files within them can have arbitrary names. However, all variable names contained across these files **must** be unique!

The app is deployed using ``narrenschiff`` tool::

  narrenschiff deploy --set-course project/tasks.yaml

After you execute this, the following happens:

1. All variables from ``vars`` files and ``chests`` are collected (only those files that are contained within the project are used - project is the directory in which the executed ``course`` is located)

  1. Load ``vars.yaml`` if it exists
  2. Load all files from the ``vars/`` directory if it exists
  3. Load and decrypt all variables from ``chest.yaml``
  4. Load all files from the ``chest/`` directory if it exists
  5. Merge all files

2. Variables are checked for duplicates, if there are any, the ship cannot take this course
3. Course file is supplied with collected variables and executed
4. Tasks are executed in sequential order, each YAML file is supplied with collected variables

You can either use ``chest.yaml`` or ``chest.yml`` file per *course project*, but not both. A *course project* is a directory where course file is located.

Treasure is encrypted using password (``key``) and salt (``spice``). These are stored in simple text files. The root of the project should contain the ``.narrenschiff.yaml`` configuration file that stores paths to these files. Keep in mind that while ``.narrenschiff.yaml`` should be source controlled, password and salt file should never be committed to your repo! Here is the example of the configuration file:

.. code-block:: yaml

  # .narrenschiff.yaml
  key: ./password.txt  # path to file containing password for encrypting files
  spice: ./salt.txt  # path to file containing salt (salt should be random and long)


.. _Jinja2: https://jinja.palletsprojects.com/en/2.10.x/

Glossary
--------

.. glossary::

  course
    Templated YAML file containing list of tasks to be performed.

  treasure
    Sensitive information, keys, secrets, and passwords are stored

  chest
    File or files in which your treasure is stored.

  key
    Master password for encrypting strings

  spice
    Salt used for encrypting strings
