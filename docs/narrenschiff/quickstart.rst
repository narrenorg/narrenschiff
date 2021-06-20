Introduction
============

``narrenschiff`` is a configuration management tool for Kubernetes inspired by Ansible. It can be used to easily source control your manifests, deployment workflows, and to encrypt secrets. In addition to encrypting secrets, it can also encrypt whole configuration files. In essence, it is a wrapper around various tools (e.g. ``helm``, and ``kubectl``). All tools are executed locally on the host OS.

Requirements
------------

* Python 3.6 or higher
* ``kubectl`` v1.20 or higher
* ``helm`` v3.0 or higher
* ``gcloud`` 343.0.0 or higher

Installation
------------

You can easily install it with ``pip``:

.. code-block:: sh

  pip install narrenschiff


We advise you to install it in virtualenv.

Quickstart
----------

To install Narrenschiff in virtualenv execute:

.. code-block:: sh

  $ mkdir infrastructure && cd infrastructure
  $ git init
  $ python3 -m venv env  && echo 'env' > .gitignore
  $ . env/bin/activate
  $ pip install narrenschiff

Initialize a course project, and encrypt a treasure:

.. code-block:: sh

  $ narrenschiff dock --autogenerate --location postgres/
  $ narrenschiff chest stash --treasure postgresPassword --value "Password123!" --location postgres/

Create a template for ``Secret`` Kubernetes resource, using encrypted treasure:

.. code-block:: sh

  $ mkdir postgres/files/
  $ cat > postgres/files/secret.yaml << EOF
  ---
  apiVersion: v1
  kind: Secret
  type: Opaque
  metadata:
    name: postgres
  data:
    POSTGRES_PASSWORD: "{{ postgresPassword | b64enc }}"
  EOF

Create a course:

.. code-block:: sh

  $ cat > postgres/course.yaml << EOF
  ---
  - name: Add secret to default namespace
    kubectl:
    command: apply
    args:
      filename:
        - secret.yaml
    namespace: "default"
  EOF

Deploy:

.. code-block:: sh

  $ narrenschiff sail --set-course postgres/course.yaml

That's it! Secret is now deployed to your cluster. Head over to `General Overview`_ to get familiar with Narrenschiff terminology, or to `Getting Started`_ to learn how to make your first project.

.. _`General Overview`: overview.html
.. _`Getting Started`: getting_started.html
