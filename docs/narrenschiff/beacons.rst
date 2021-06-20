Beacons
=======

If you only want to execute a part of the course, then you should use beacons. Beacons are essentially tags on you tasks that allow you to create special paths of execution.

.. note::

  We advise you to test the example using Minikube. You can find instructions on how to setup Minikube here_ and also in the `official documentation`_.

Let's look at simple example:

.. code-block:: yaml

  # examples/stats/course.yaml
  - name: List all namespaces
    kubectl:
      command: get namespaces
    beacons:
      - always

  - name: List all pods in default namespace
    kubectl:
      command: get pods
      args:
        namespace: default
    beacons:
      - default

  - name: List all pods in kube-system namespace
    kubectl:
      command: get pods
      args:
        namespace: kube-system
    beacons:
      - kube-system

Beacons are passed to ``narrenschiff`` with ``--follow-beacons`` flag, like so:

.. code-block:: sh

  $ narrenschiff sail --follow-beacons default --set-course examples/stats/course.yaml

  * [ 2020-07-20 10:47:36.901965 ] * [ List all namespaces ] ******************

  NAME              STATUS   AGE
  default           Active   2d17h
  kube-node-lease   Active   2d17h
  kube-public       Active   2d17h
  kube-system       Active   2d17h


  * [ 2020-07-20 10:47:36.959850 ] * [ List all pods in default namespace ] ***

  NAME                        READY   STATUS    RESTARTS   AGE
  postgres-7bf8d6b875-hp58b   1/1     Running   1          2d15h

What happened? ``always`` is a reserved beacon in Narrenschiff. When you execute a course, if you have any task tagged with ``always`` it will always execute in addition to the tasks targeted by supplied beacon. In this case, we chose to execute only those tasks marked with ``default`` i.e. ``--follow-beacons default``.

A task can be marked with multiple becaons e.g.

.. code-block:: yaml

  beacons:
    - dev
    - stage
    - prod

And you can also select multiple becaons from the command line:

.. code-block:: sh

  $ narrenschiff sail --follow-beacons dev,stage --set-course course.yaml

Here's a practical example. If you are using Helm to manage you applications, you can pack the upgrade instructions in a single course, but separate environments using becaons.

.. code-block:: yaml

  # helm/postgres.yaml
  - name: Add bitnami repo to Helm
    helm:
      command: repo add jetstack https://charts.bitnami.com/bitnami
    beacons:
      - always

  - name: Update repo
    helm:
      command: repo update
    beacons:
      - always

  - name: Upgrade Postgres on development
    helm:
      command: upgrade
      name: postgres
      chart: bitnami/postgresql
      version: 11.8.0
      opts:
        - atomic
        - cleanup-on-fail
        - reuse-values
      args:
        namespace: development
        values:
          - "{{ values | secretmap }}"
    beacons:
      - dev

  - name: Upgrade Postgres on staging
    helm:
      command: upgrade
      name: postgres
      chart: bitnami/postgresql
      version: 9.1.1
      opts:
        - atomic
        - cleanup-on-fail
        - reuse-values
      args:
        namespace: staging
        values:
          - "{{ values | secretmap }}"
    beacons:
      - stage

  - name: Upgrade Postgres on production
    helm:
      command: upgrade
      name: postgres
      chart: bitnami/postgresql
      version: 9.1.1
      opts:
        - atomic
        - cleanup-on-fail
        - reuse-values
      args:
        namespace: production
        values:
          - "{{ values | secretmap }}"
    beacons:
      - prod

Now, if you want to upgrade only your service on the development environment, you can do this without executing other tasks in the course:

.. code-block:: sh

  $ narrenschiff sail --follow-becaons dev --set-course helm/postgres.yaml

Beacons can only be used on tasks. They cannot be used on course imports (i.e. ``import_course`` does not support becaons).

.. _here: getting_started.html#before-you-start
.. _`official documentation`: https://kubernetes.io/docs/tasks/tools/install-minikube/
