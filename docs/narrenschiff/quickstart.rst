Introduction
============

``narrenschiff`` is a configuration management tool for Kubernetes. It can be used to easily source control your manifests, and to actually encrypt your ``Secret`` resources. In addition to encrypting secrets, it can also encrypt whole configuration files. In essence, it is a wrapper around various tools (e.g. ``helm``, and ``kubectl``). All tools are executed locally on the host OS.

Requirements
------------

* Python 3.6 or higher
* ``kubectl`` v1.17 or higher
* ``helm`` v3.0 or higher
* ``gcloud`` 297.0.1 or higher

Installation
------------

You can easily install it with ``pip``:

.. code-block:: sh

  pip install narrenschiff


We advise you to install it in virtualenv.

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
          - namespaces.yaml  # filenames are referenced relative to files/ dir
          - rbac.yaml

Each YAML file in the project is treated as a template file i.e. each ``course`` can have template variables. Template language that is powering ``courses`` is Jinja2_.

File paths are referenced relative to the ``files/`` directory in the *course project* root. ``files/`` is reserved for Jinja2 templates of Kubernetes manifest files.

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

You can use ``vars.yaml`` and ``chest.yaml`` to define variables for you project. ``vars.yaml`` file or ``vars/`` directory contain unencrypted variables. ``chest.yaml`` file or ``chest/`` directory is a place to stash your *treasure* (i.e. keys, secrets, passwords, etc.). Both ``vars/`` and ``chest/`` directories can have arbitrary nesting and files within them can have arbitrary names. However, all variable names contained across these files **must** be unique! All boolean values must be quoted.

Chest files have flat dictionary structure. No nesting of the keys is allowed (at the moment at least):

.. code-block:: yaml

  db_password: 6Wziywgso3YsosQNfMeufodDZxEaOyujHM+ch9Pxe5u1u2ZO5e7G9bPOhEIVYo8n
  hash_key: uSn/rKMdbMArR0SnWcbtP1Z64/Y8LI8LNOZGbVZUmm5ioFLV/NwP6OcyTNGgMSGi

The app is deployed using ``narrenschiff`` tool::

  narrenschiff sail --set-course project/tasks.yaml

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

You can also encrypt files and bring them into your source code. Files are encrypted, and stored at desired location, and relative path to the file is saved in `secretmap` file.

If you have a fairly complex course, and you want to execute only a specific set of tasks, you can use `beacons`:

.. code-block:: yaml

  - name: List all namespaces
    kubectl:
      command: get namespaces

  - name: List all pods
    kubectl:
      command: get pods
    beacons:
      - always
      - pods

  - name: Check pod resources
    kubectl:
      command: top pods
    beacons:
      - stats
      - pods

  - name: Check node resources
    kubectl:
      command: top nodes
    beacons:
      - stats

Now you can easily select which collection of tasks you want to execute:

.. code-block:: sh

  narrenschiff sail --set-course stats.yaml --follow-beacons stats,pods

Note that ``always`` is a special keyword for beacons! Taks marked with ``always`` are always executed, regardless of the becaons you specified on the command line.

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

  secretmap
    Encrypted file (currently only supported for ``helm`` module)
