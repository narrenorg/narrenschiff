General Overview
================

Basic unit of ``narrenschiff`` is a ``course`` i.e. file or group of files storing tasks that are to be performed in sequential order. ``course`` is YAML file e.g.:

.. code-block:: yaml

  - name: Deploy config map
    kubectl:
      command: apply
      args:
        filename: "configmap.yaml"

  - name: Apply namespaces and RBAC settings
    kubectl:
      command: apply
      args:
        filename:
          - namespaces.yaml  # filenames are referenced relative to files/ dir
          - rbac.yaml

Each YAML file in the project is treated as a template file i.e. each ``course`` can have template variables. Template language that is powering Narrenschiff is Jinja2_.

File paths are referenced relative to the ``files/`` directory in the *course project* root. ``files/`` is reserved for Jinja2 templates of Kubernetes manifests.

The basic directory layout should resemble something like this::

  infrastructure/  <-- root project (all commands are executed from here)
  ├── .narrenschiff.yaml  <-- root project configuration
  └── webapp  <-- course project
      ├── files  <-- Templates for you manifest files
      │   ├── app
      │   │   ├── configmap.yaml
      │   │   └── deployment.yaml
      │   ├── db
      │   │   ├── deployment.yaml
      │   │   └── secret.yaml
      │   ├── namespaces.yaml
      │   └── rbac.yaml
      ├── chest  <-- directory with arbitrary nesting may be used in addition to chest.yaml
      │   ├── database.yaml
      │   └── secrets.yaml
      ├── vars  <-- directory with arbitrary nesting may be used in addition to vars.yaml
      │   ├── common.yaml
      │   ├── domains.yaml
      │   └── apps
      │       └── prod.yml
      ├── overrides  <-- encrypted helm values.yaml overrides i.e. secretmaps
      │   └── values.yaml
      ├── tasks.yaml  <-- course file describing the deployment process
      ├── secretmap.yaml  <-- paths to encrypted files
      ├── chest.yaml  <-- encrypted variables
      └── vars.yaml  <-- cleartext variables

``files/`` directory is a directory reserved for your Kubernetes manifests. With ``narrenschiff`` you can use Jinja2 templating language to inject variables into the manifests.

You can use ``vars.yaml`` and ``chest.yaml`` to define variables for you project. ``vars.yaml`` or ``vars/`` directory contains unencrypted variables. ``chest.yaml`` or ``chest/`` directory is a place to stash your *treasures* (i.e. keys, secrets, passwords, etc.). Both ``vars/`` and ``chest/`` directories can have arbitrary nesting and files within them can have arbitrary names. However, all variable names contained across these files **must** be unique! All boolean values must be quoted.

You can also encrypt files and commit them to your source code safely. Files are encrypted, and stored at desired location, and relative paths to the files are saved in ``secretmap.yaml``. For example, when you deploy a Helm chart, it is often common to override default ``values.yaml``. However, this is unencrypted file which can be used to configure secrets. You can stash your ``values.yaml`` override as a secretmap, and commit it to the source code without any worry of passwords and secrets leaking.

Chest files have flat dictionary structure. No nesting of the keys is allowed:

.. code-block:: yaml

  dbPassword: 6Wziywgso3YsosQNfMeufodDZxEaOyujHM+ch9Pxe5u1u2ZO5e7G9bPOhEIVYo8n
  hashKey: uSn/rKMdbMArR0SnWcbtP1Z64/Y8LI8LNOZGbVZUmm5ioFLV/NwP6OcyTNGgMSGi

The app is deployed as:

.. code-block:: sh

  $ narrenschiff sail --set-course webapp/tasks.yaml

After you execute this, the following happens:

1. All variables from ``vars`` files, ``chests``, and ``secretmaps`` are collected (only those files that are contained within the course project are used - course project is the directory in which the executed ``course`` is located)

  1. Load ``vars.yaml``
  2. Load all files from the ``vars/`` directory if it exists
  3. Load and decrypt all variables from ``chest.yaml``
  4. Load all files from the ``chest/`` directory if it exists
  5. Load all variables from ``secretmap.yaml``
  6. Merge all files

2. Variables are checked for duplicates, if there are any, the ship cannot take this course
3. Course file is supplied with collected variables and executed
4. Tasks are executed in sequential order, each YAML file is supplied with collected variables, and secretmaps are decrypted

You can either use ``chest.yaml`` or ``chest.yml`` file per *course project*, but not both. Choose one extension, and stick to it. A *course project* is a directory where course file is located.

Treasure is encrypted using password (``key``) and salt (``spice``). These are stored in simple text files. The root of the project must contain the ``.narrenschiff.yaml`` configuration file that stores paths to these files. Keep in mind that while ``.narrenschiff.yaml`` should be source controlled, password and salt file should never be committed to your repo! Here is the example of the configuration file:

.. code-block:: yaml

  # .narrenschiff.yaml
  key: ~/.infrastructure/password.txt  # path to file containing password for encrypting files
  spice: ~/.infrastructure/salt.txt  # path to file containing salt (salt should be random and long)

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

Note that ``always`` is a special keyword for beacons! Tasks marked with ``always`` are always executed, regardless of the becaons you specified on the command line.

.. _Jinja2: https://jinja.palletsprojects.com/en/2.10.x/

Glossary
--------

.. glossary::

  course
    Templated YAML file containing list of tasks to be performed.

  course project
    Directory in which the main course is located. This directory also contains ``vars.yaml``, ``chest.yaml``, ``secretmap.yaml``, and other files needed to run the course.

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
