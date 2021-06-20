Getting Started
===============

This guide will lead you from set up of a project to deployment of a service. You can follow this guide using a custom namespace in your existing cluster or, better yet, using Minikube. You need to have ``kubectl`` installed in order for ``narrenschiff`` to work. **Everything you write using** ``narrenschiff`` **will be executed locally** on the host operating system (just as you would execute ``kubectl`` or ``helm`` locally).

Before you Start
----------------

We advise you to test this tool using Minikube. This section will briefly cover how to setup and use Minikube, and how to switch between contexts (i.e. clusters).

Execute following comands in order to install Minikube:

.. code-block:: sh

  curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
  sudo cp minikube /usr/local/bin/minikube
  sudo chmod +x /usr/local/bin/minikube

When starting Minikube ``kubectl`` should automatically change contexts (i.e. the cluster the ``kubectl`` is associated with). You can check the current context with:

.. code-block:: sh

  kubectl config current-context

And you can switch to your context with:

.. code-block:: sh

  kubectl config use-context <CONTEXT_NAME>

Start Minikube with:

.. code-block:: sh

  minikube start --driver=docker

You can stop and delete cluster with:

.. code-block:: sh

  minikube stop
  minikube delete

Setting up a Project
--------------------

There are two ways to start a project. Manually, and using a built in ``narrenschiff dock`` command. We advise you to set your projects manually. If this is your first time you are using ``narrenschiff``, please review the following section, as it describes the fundamental anatomy of a project.

Manually
********

Start managing your infrastructure by first laying out a basic directory structure:

.. code-block:: sh

  mkdir infrastructure
  cd infrastructure
  git init
  pipenv python --three
  pipenv install narrenschiff
  mkdir project
  touch project/course.yaml
  touch project/vars.yaml
  touch project/chest.yaml
  touch project/secretmap.yaml
  touch .narrenschiff.yaml

All course projects will be managed in subdirectories of ``infrastructure/`` (consider this to be your *main project*). In the root of your infrastructure repo you need to place a ``.narrenschiff.yaml`` configuration file. This configuration file contains password (key) and salt (spice) that are used to encrypt all files and strings accross all of your course projects.

Each course project needs to contain special files that are used to store cleartext and cyphertext variables. These are:

* ``vars.yaml`` - Used to store variables in cleartext
* ``chest.yaml`` - Used to store encrypted variables
* ``secretmap.yaml`` - Used to store paths to encrypted files

All variables contained in these files are injected in your templates when you start deploying with narrenschiff. There is one rule that you need to remember: **no duplicates are allowed**! See `Vars Files`_ for detailed explanation.

Last file that needs to be explained is ``course.yaml``. The name of this file can be arbitraty, and you can have multiple of these. This is actually the file which contains configuration, deployment, and other instructions. In essence a ``course`` is the most basic unit of ``narrenschiff``. ``course`` files are YAML files that contain list of tasks to be performed written using a special syntax. Consequently, the project which contains course files, is called a *course project*. In this example a course project is ``project/``.

``narrenschiff dock``
*********************

You can easily start a project using ``narrenschiff dock``. It is advisable to run ``narrenschiff`` from virtualenv. For this example, we'll use ``pipenv`` but you can use any other dependency management too:

.. code-block:: sh

  mkdir infrastructure
  cd infrastructure
  git init
  pipenv python --three
  pipenv install narrenschiff
  pipenv shell
  narrenschiff dock --location project --autogenerate

This will create a *course project* on path ``project/``. ``--autogenerate`` flag will generate *key* and *spice* for the project (in the home directory of the user), and add them to ``.narrenschiff.yaml``.

Configuring a Project
---------------------

Configuration of a project is fairly simple. You only need to setup ``.narrenschiff.yaml`` and accompanying files for *key* and *spice*. If you've used ``narrenschiff dock`` this should already be done for you. However, when you're setting up a main project manually, you'll have to do this step manually too.

*Key* and *spice* must not be commited into your source code! Store them somewhere else. They are usually stored in the home directory of a user executing ``narrenschiff``:

.. code-block:: sh

  mkdir ~/.infrastructure
  cd ~/.infrastructure
  head -c 30 /dev/urandom | base64 > password.txt
  head -c 30 /dev/urandom | base64 > salt.txt

Now you can update your configuration file:

.. code-block:: yaml

  # Paste this into your .narrenschiff.yaml configuration file
  key: ~/.infrastructure/password.txt
  spice: ~/.infrastructure/salt.txt


Deploying Your First Service
----------------------------

As an example, we will deploy PostgreSQL. Typically, you deploy database as ``StatefulSet``, however in this example we will stick to simple ``Deployment``, just to make our life easier. Execute this commands from your *main project*:

.. code-block:: sh

  mkdir -p postgres/files
  touch postgres/course.yaml
  touch postgres/vars.yaml
  touch postgres/chest.yaml
  touch postgres/secretmap.yaml
  touch postgres/files/deployment.yaml
  touch postgres/files/secret.yaml
  touch postgres/files/configmap.yaml

The way you would usually run postgres in a docker is like so:

.. code-block:: sh

  docker run --name postgres \
    -e POSTGRES_USER=user \
    -e POSTGRES_PASSWORD=password \
    -e POSTGRES_DB=db \
    -d postgres:latest

When translating this to Kubernetes manifests, we obviously need to split this into several resources: ``Deployment`` (for the container itself), ``ConfigMap`` (for database name and user name), and ``Secret`` (for password). We will place all these manifests in ``files/`` directory in the *course project*. In ``narrenschiff``, ``files/`` within a *course project* is reserved for Kubernetes manifests. You can write these configuration using Jinja2 templating language, and ``narrenschiff`` will inject variables from vars files into the manifests.

Let's write Kubernetes manifests. ``ConfigMap`` is straightforward:

.. code-block:: yaml

  # postgres/files/configmap.yaml
  ---
  apiVersion: v1
  kind: ConfigMap
  metadata:
    name: postgres
    labels:
      app: postgres
  data:
    POSTGRES_USER: user
    POSTGRES_DB: db


Nothing new here. However, for the secret, we want to utilize encryption. Normally, secrets in Kubernetes are not encrypted in manifests (only base64 encoded). The original reason ``narrenschiff`` was made is precisely to overcome this problem - so we can encrypt a secret and source control our infrastructure without compromising it. We'll use ``narrenschiff chest`` to encrypt our password, and store it in the ``chest.yaml``.

.. code-block:: sh

  narrenschiff chest stash --location postgres/ --treasure postgresPassword --value Password123!

If you take a look inside ``chest.yaml`` you'll find your secret:

.. code-block:: sh

  cat postgres/chest.yaml
  postgresPassword: 3GghhpUTDrGvGroyhO5J/4TLlpSKUX1hBn3FkgLVd/vq0n6dgCD8+nEB08kYdd2G

The name of our secret variables is ``postgresPassword``. And we can use it now anywhere in our manifests. But naturally, we'll use it to define a ``Secret``:

.. code-block:: yaml

  # postgres/files/secret.yaml
  ---
  apiVersion: v1
  kind: Secret
  type: Opaque
  metadata:
    name: postgres
    labels:
      app: postgres
  data:
    POSTGRES_PASSWORD: "{{ postgresPassword | b64enc }}"

You'll notice that instead of usual base64 encoded string we have ``"{{ postgresPassword | b64enc }}"``. This is Jinja2 syntax. It says "hey, replace what's between the double curly braces, and then apply the ``b64enc`` filter". When you execute deployment with ``narrenschiff sail``, all secrets accross chest files will be collected, decrypted, and passed to Jinja2 templates for rendering. Then, Jinja2 will replace this secret in a template, but not before passing it through ``b64enc`` filter (which encodes string with base64). The end product is what you would normally write as a configuration, the only difference being, you can now safely commit it, and track it with source control, without worrying about secrets being leaked. Only people with *key* and *spice* can decrypt a secret.

This is how it will actually look when rendered:

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
      POSTGRES_PASSWORD: "UGFzc3dvcmQxMjMhCg=="

But you don't really need to be concerned with how it looks when rendered. Finally, we'll define a ``Deployment``:

.. code-block:: yaml

  # postgres/files/deployment.yaml
  ---
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: postgres
    labels:
      app: postgres
  spec:
    replicas: 1
    selector:
      matchLabels:
        app: postgres
    template:
      metadata:
        labels:
          app: postgres
      spec:
        containers:
        - name: postgres
          image: postgres:latest
          ports:
          - containerPort: 5432
          envFrom:
            - configMapRef:
                name: postgres
            - secretRef:
                name: postgres

For example, if you want to pin down the version of the postgres, and be able to update it easily later, you can replace ``image: postgres:latest`` with ``image: "{{ postgresDockerImage }}"``, and add to your ``vars.yaml`` specifig version as: ``postgresDockerImage: "posgres:12-alpine"``.

Now, all we have to do is to deploy this to our cluster. We would usually do this like so:

.. code-block:: sh

  kubectl appyl -f secret.yaml,configmap.yaml,deployment.yaml --namespace default

However, we don't have ordinary Kubernetes manifests anymore. Now we're using templated manifests. Therefore we need to write the equivalent command using Narrenschiff. Open ``course.yaml`` and write the following:

.. code-block:: yaml

  # postgres/course.yaml
  - name: Deploy postgres
    kubectl:
      command: apply
      args:
        filename:
          - secret.yaml
          - configmap.yaml
          - deployment.yaml
        namespace: "default"

In Narrenschiff, this is called a *taks*, and *course* is a collection of tasks.

Now, all you have to do is to deploy this to our cluster. Or, in other words, set a course and sail this crazy ship:

.. code-block:: sh

  narrenschiff sail --follow-course postgres/course.yaml

The output should be similar to this:

.. code-block:: sh

  * [ 2020-07-17 19:33:27.852325 ] * [ Deploy postgres ] ***************

  secret/postgres created
  configmap/postgres created
  deployment.apps/postgres created

.. _`Vars Files`: vars_files.html
