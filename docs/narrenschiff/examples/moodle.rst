Deploying Moodle and MariaDB using Helm
=======================================

This example will show you how to use secretmaps and Narrenschiff helm module in order to deploy two services to the cluster.

Before you Start
----------------

We advise you to use Minikube as you follow along this tutorial. Minikube is easy to setup, and manage. See the installation process in the `official documentation`_, or see our `getting started`_ tutorial.

You can find the source code for this tutorial in the official Narrenschiff repo_ under the ``examples/`` directory. The example in the repo uses ``.narrenschiff.yaml`` configuration from the repo itself. But, for completeness, we will show you how to properly start a project.

Start the Project
-----------------

Start by installing Narrenschiff and making a project.

.. code-block:: sh

  $ mkdir moodle && cd moodle
  $ git init
  $ python3 -m venv env  && echo 'env' >> .gitignore
  $ . env/bin/activate
  $ pip install narrenschiff

Now you are ready to make a course project. In the root project, execute following command:

.. code-block:: sh

  $ narrenschiff dock --autogenerate --location moodle

Stash Your Treasure in a Chest
------------------------------

When deploying application with helm, you can use ``--set`` to set values on the comand line, or ``--values`` to read in values from a file. ``--set`` is useful when you want to edit a single value, but when you need to enter more complex configuration, you would use ``--values``.

Because we need to supply database password in two different charts, we will use ``--set`` to supply it at course runtime. However, all other values specific to the charts themselves can be configured with ``--values``.

Therefore we will start with the most basic. Stashing our MariaDB password in the course chest.

.. code-block:: sh

  $ narrenschiff chest stash --location moodle/ --treasure databasePassword --value 'Password123!'

Prepare Overrides for values.yaml
---------------------------------

Narrenschiff's helm module can work with ``values.yaml``. But by default, these files need to be encrypted. Values file oftentime contains sensitive information such as passwords, so it's better to have it encrypted. Make the ``overrides/`` directory in your course file, and make these two files within it:

.. code-block:: yaml

  # moodle/overrides/mariadb.yaml
  ---
  replication:
    enabled: false

  master:
    resources:
      limits:
        cpu: 500m
        memory: 512Mi
      requests:
        cpu: 50m
        memory: 128Mi

    livenessProbe:
      enabled: false
    readinessProbe:
      enabled: false

    persistence:
      enabled: true
      mountPath: /bitnami/mariadb
      accessModes:
        - ReadWriteOnce
      size: 500Mi

  # moodle/overrides/moodle.yaml
  ---
  moodleUsername: admin
  moodlePassword: Password123!
  moodleEmail: admin@moodle.local

  mariadb:
    enabled: false
    secret:
      requirePasswords: false

  livenessProbe:
    enabled: false
  readinessProbe:
    enabled: false

  service:
    type: NodePort
    port: 80
    httpsPort: 443
    nodePorts:
      http: "30080"
      https: "30443"
    externalTrafficPolicy: Cluster

  ingress:
    enabled: false
    certManager: false
    hostname: moodle.local

  persistence:
    enabled: true
    accessMode: ReadWriteOnce
    size: 500Mi

  resources:
    requests:
      memory: 512Mi
      cpu: 500m

Encrypt them using:

.. code-block:: sh

  $ narrenschiff secretmap stash --source moodle/overrides/mariadb.yaml --destination overrides/mariadb.yaml --treasure mariadb --location moodle
  $ narrenschiff secretmap stash --source moodle/overrides/moodle.yaml --destination overrides/moodle.yaml --treasure moodle --location moodle

If you inspect your secretmap file, you will see that it contains paths to the encrypted files:

.. code-block:: sh

  $ cat moodle/secretmap.yaml
  mariadb: overrides/mariadb.yaml
  moodle: overrides/moodle.yaml

Update ``vars.yaml``
--------------------

It's a good idea to respect DRY principle in your course files. For this purpose, we will utilize ``vars.yaml`` and define common cleartext variables:

.. code-block:: yaml

  # moodle/vars.yaml
  namespace: default

  database:
    user: moodle
    name: moodle

Deploy
------

Before deployment, we have to write the course:

.. code-block:: yaml

  # moodle/course.yaml
  ---
  - name: Add bitnami repo
    helm:
      command: repo add bitnami https://charts.bitnami.com/bitnami

  - name: Update helm repo
    helm:
      command: repo update

  - name: Install MariaDB database
    helm:
      command: upgrade
      name: mariadb
      chart: bitnami/mariadb
      opts:
        - install
        - atomic
        - cleanup-on-fail
      args:
        namespace: "{{ namespace }}"
        version: 7.9.2
        values:
          - "{{ mariadb | secretmap }}"
        set:
          - "db.user={{ database.user }}"
          - "db.password={{ databasePassword }}"
          - "db.name={{ database.name }}"

  - name: Install Moodle
    helm:
      command: upgrade
      name: moodle
      chart: bitnami/moodle
      opts:
        - install
        - atomic
        - cleanup-on-fail
      args:
        namespace: "{{ namespace }}"
        version: 8.1.1
        values:
          - "{{ moodle | secretmap }}"
        set:
          - "externalDatabase.user={{ database.user }}"
          - "externalDatabase.password={{ databasePassword }}"
          - "externalDatabase.database={{ database.name }}"
          - "externalDatabase.host=mariadb.{{ namespace }}.svc.cluster.local"


Finally apply changes to the cluster:

.. code-block:: sh

  $ narrenschiff sail --set-course moodle/course.yaml

Verify
------

You can verify that Moodle is deployed by accessing it through your web browser:

.. code-block:: sh

  $ minikube service moodle --url

Use ``minikube stop && minikube delete`` to stop and delete the cluster.

.. _`official documentation`: https://kubernetes.io/docs/tasks/tools/install-minikube/
.. _`getting started`: ../getting_started.html
.. _repo: https://github.com/petarGitNik/narrenschiff
