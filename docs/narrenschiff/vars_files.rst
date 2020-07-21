Vars Files
==========

There are three types of variable files in Narrenschiff:

* ``vars`` - plain variables i.e. non-encrypted variables
* ``chest`` vars - encrypted variables
* ``secretmap`` vars - variables that store paths to files encrypted with Narrenschiff

Plain Variables
---------------

These are the most basic of all variable types. Plain variables give you ability to easily reuse variables accross your templates. These variables also support arbitraty nesting of variables.

.. code-block:: yaml

  # vars.yaml
  cluster_name: clusty-mc-cluster  # simple "flat" variable
  namespaces:  # variable with nesting
    dev: development
    stage: staging
    prod: production

Now you can use these variables anywhere in your course files, or in any template file located in `files/`. For example:

.. code-block:: yaml

  # course to create a cluster
  ---
  - name: Cluster create
    gcloud:
      command: "container clusters create {{ cluster_name }}"
      args:
        num-nodes: 3

In the following example we will use the Jinja2 templating feature to loop through nested variable, and create Kubernetes resources accross multiple namespace in one file (instead of writing multiple files):

.. code-block:: jinja

  # files/namespaces.yaml
  {% for key, value in namespaces.items() -%}
  ---
  apiVersion: v1
  kind: Namespace
  metadata:
    name: "{{ value }}"
    labels:
      name: "{{ value }}"
  {% endfor %}

Plain vars are stored in ``vars.yaml`` or in ``vars/`` directory. If you are using ``vars/`` directory, you can name vars files within it whatever you want, and nest them however you need. The only rule you have to remember is that variable names must be unique accross all vars files (you can't have variable with the same name in chests, and in vars, or secretmaps).

Since vars files (and chests too) are YAML files, all boolean values must be quoted.

Chest
-----

Chest variables behave similar to plain variables. However, there are two important differences:

* You have a command line tool to manage them
* Chest vars don't support arbitrary nesting (they have a flat dictionary structure)

You can also use ``chest.yaml`` as well as ``chest/`` directory with custom named files. However, same rules apply for chest variables: they have to be unique accross all vars files.

.. code-block:: yaml

  # chest.yaml
  # the following two are ok:
  db_password: enSkvMbU3Sa3YimjyqR3rskZHx3tUYlIpC5U1Xpo3k/qntCCp+HyJfTtjg++tSTF
  hashing_key: j9gc0niSm1ADGK/95jVr7ugeUe87wDsCBhUp1zGtw3oJ4nz+h9JJKHfHdmYWFz8b

  # nesting of variables is not supported for chest files!
  mistery:  # this is NOT OK
    db_password: enSkvMbU3Sa3YimjyqR3rskZHx3tUYlIpC5U1Xpo3k/qntCCp+HyJfTtjg++tSTF
    hashing_key: j9gc0niSm1ADGK/95jVr7ugeUe87wDsCBhUp1zGtw3oJ4nz+h9JJKHfHdmYWFz8b

When using secrets in your templates, there is no any special step that you have to take in order to decrypt them. Narrenschiff does that for you when it collects all the variables. However, when you're using them with secret files, you have to obey Kubernetes way of writing ``Secret`` resources, so you'll have to base64 encode them. Narrenschiff offers you a custom Jinja filter (``b64enc``) to easily to that:

.. code-block:: yaml

  ---
  apiVersion: v1
  kind: Secret
  type: Opaque
  metadata:
    name: postgres
    labels:
      app: postgres
  data:
    DB_PASSWORD: "{{ db_password | b64enc }}"
    SECRET_KEY: "{{ hashing_key | b64enc }}"

``narrenschiff chest`` offers you a number of ways to work with secrets. You can either encrypt them on the command line, and paste them into chest files yourself (with ``narrenschiff chest lock`` and ``narrenschiff chest unlock``), or you can dynamicall update ``chest.yaml`` (with ``narrenschiff chest stash`` and ``narrenschiff chest loot``).

Lock and unlock are useful when you want to try things out. They don't require a location to use, only that you're executing them from the root project.

.. code-block:: sh

  $ narrenschiff chest lock --value 'password'
  enSkvMbU3Sa3YimjyqR3rskZHx3tUYlIpC5U1Xpo3k/qntCCp+HyJfTtjg++tSTF
  $ narrenschiff chest lock --value 'key'
  j9gc0niSm1ADGK/95jVr7ugeUe87wDsCBhUp1zGtw3oJ4nz+h9JJKHfHdmYWFz8b
  $ narrenschiff chest unlock --value enSkvMbU3Sa3YimjyqR3rskZHx3tUYlIpC5U1Xpo3k/qntCCp+HyJfTtjg++tSTF
  password
  $ narrenschiff chest unlock --value j9gc0niSm1ADGK/95jVr7ugeUe87wDsCBhUp1zGtw3oJ4nz+h9JJKHfHdmYWFz8b
  key

However, it's often more easier to update ``chest.yaml`` dynamically, and not worry about whether you copy/pasted whole string from the command line (are you sure you haven't missed that first or last character when selecting?):

.. code-block:: sh

  $ narrenschiff chest stash --treasure db_password --value password --location project/
  $ narrenschiff chest loot --treasure db_password --location project/

Also if you want to update ``chest.yaml`` with treasure that lies on your filesystem, you can test if the encryption works with ``lock`` and ``unlock``:

.. code-block:: sh

  $ narrenschiff chest lock --value "$( cat ~/Downloads/service-account.json )"

And you can stash it automatically with:

.. code-block:: sh

  $ narrenschiff chest stash --location project/ --treasure service_account --value "$( cat ~/Downloads/service-account.json )"

If you're in a hurry and you'll need to skim through all variables to find something, you can dump all chest variables to STDOUT with ``narrenschiff chest dump``:

.. code-block:: sh

  $ narrenschiff dump --location examples/

    db_password: password
    hashing_key: key

Secretmap
---------

Secretmap variables store paths to encrypted files. Encrypted files don't support Jinja2 templating, and they are only reserved for use with the ``helm`` module.

These variables are stashed in ``secretmap.yaml``, and this file can only be dynamically updated.

The most basic of commands is ``narrenschiff secretmap stash``

.. code-block:: sh

  $ narrenschiff secretmap stash --treasure dev_values --location project/ --source ~/repos/source/dev.yaml --destination overrides/dev.yaml
  $ tree project/
  project/
  ├── overrides
  │   └── dev.yaml
  ├── secretmap.yaml
  └── course.yaml

As you can see, ``--destination`` is a *path relative to the root of the course project*. Note, it is **not** a path relative to the root project of your infrastructure (where ``.narrenschiff.yaml`` file is located). The course project is project that contains in its root files such as ``secretmap.yaml`` and ``chest.yaml``. So, in other words, it's a path relative to the ``secretmap.yaml``. ``--source`` on the other hand, can be any path on your filesystem. After encryption if you inspect ``dev.yaml`` in ``overrides/``, you'll se that content of the file has been indeed encrypted. And if you inspect ``secretmap.yaml`` you'll find a relative path to the encrypted file:

.. code-block:: sh

  $ cat project/secretmap.yaml
  dev_values: overrides/dev.yaml

How do you reference this in your Narrenschiff configuration? When ``narrenschiff sail`` gets executed, it needs to decrypt the file before it can be used. We instruct Narrenschiff that following variable is not a simple variable, but a path to a file, with a custom narrenschiff Jinja2 filter:

.. code-block:: yaml

  - name: Install Prometheus
    helm:
      command: install
      name: redis
      chart: bitnami/redis
      version: 10.7.11
      opts:
        - atomic
      args:
        namespace: development
        values:
          - "{{ dev_values | secretmap }}"

Therefore, when working with secretmaps, you'll have to pipe your variable to ``secretmap`` filter in your courses i.e. ``{{ dev_values | secretmap }}``.

The inverse operation of stash is loot. You can decrypt a file and place it somewhere on your filesystem with:

.. code-block:: sh

  $ narrenschiff secretmap loot --treasure dev_values --location project/ --destination /tmp/dev.yaml

However, editing file in such a way is cumbersome. Fortunately, we have ``alter`` available. It will open a file in your preferred editor (or ``vi``):

.. code-block:: sh

  $ narrenschiff secretmap alter --treasure dev_values --location project/

If you want to change default editor, change ``EDITOR`` environment variable to preferred editor.

Sometimes you just want to preview the file. Narrenschiff got you covered here also. Use ``peek`` to dump file content to STDOUT:

.. code-block:: sh

  $ narrenschiff secretmap peek --treasure dev_values --location project/

When you have many secretmaps in a course project, it's really hard to peek and manually search through all of them. Narrenschiff gives you ability to grep over those encrypted files with ``search``:

.. code-block:: sh

  $ narrenschiff secretmap search --match "ClusterIP" --location project/

A really powerful feature of Narrenschiff secretmap search is that match pattern can be a Python regex expression.

And finally, you can delete secretmaps with:

.. code-block:: sh

  $ narrenschiff secretmap destroy --treasure dev_values --location project/

Rules
-----

There is one rule that you need to remember: **no duplicates are allowed**! ``narrenschiff`` collects all variables in all var files, and if you have duplicate values, the program will exit with an error. And also you should also keep in mind this tiny rule:

1. All variables from ``vars`` files, ``chests``, and ``secretmap`` are collected (only those files that are contained within the *course project* are used)

  1. Load ``vars.yaml``
  2. Load all files from the ``vars/`` directory if it exists
  3. Load and decrypt all variables from ``chest.yaml``
  4. Load all files from the ``chest/`` directory if it exists
  5. Load all variables from ``secretmap.yaml``
  6. Merge all files

2. Variables are checked for duplicates, if there are any ``narrenschiff sail`` will fail

Jokes aside, there is no variable file precedence as in Ansible_. All vars files are created equal, and each treasure within it is unique. If you have duplicates, Narrenschiff will let you know, so you can fix this. Not having to think about vars file precedence `streamlines thought process`_, leaving you more time to think about your infrastructure, rather than the quirks of the tool you're using.

.. _Ansible: https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#variable-precedence-where-should-i-put-a-variable
.. _`streamlines thought process`: https://www.artima.com/weblogs/viewpost.jsp?thread=98196
