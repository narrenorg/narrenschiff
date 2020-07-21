Courses
=======

A course in Narrenschiff is a collection of tasks. A single task corresponds to a single command line you would typically execute using e.g. ``kubectl`` or ``helm``.

This is a general anatomy of a task:

.. code-block:: yaml

  - name: Deploy nginx container with basic auth  # name of the task (required)
    kubectl:  # module you're using (required)
      command: apply
      args:
        filename:
          - nginx/app/secret.yaml
          - nginx/app/configmap.yaml
          - nginx/app/deployment.yaml
        namespace: default
    beacons:  # tags for alternative execution path (optional)
      - dev  # chose whatever value ("always" is a reserved becaon)

``name`` of the task describes what task should do, and with module you're actaully writing what the task is doing. Names are required, so your infrastructure configuration becomes a self-documenting repo. Name is an arbitraty description. Module, however, can only be whatever is implemented in Narrenschiff. At this moment, there are several modules available to use:

* ``kubectl``
* ``helm``
* ``gcloud``
* ``kustomization``
* ``wait_for_pod``

At this point, all modules are considered to be experimental and in beta.

Everything nested under module (in this case command, args, filename, namespace) is unique to the module. These options are covered in the module documentation.

``beacons`` are optional, and they provide you a way for alternative execution path of your course. In other words, you can choose which part of the course you want to execute using becaons. Since they are optional, if you don't need them, don't add them. See `Beacons`_ for detailed overview.

Tasks in a course are executed sequentially. When you execute a course with ``narrenschiff sail`` all variables are gathered, templates rendered, and task collected in ordered list, and executed one by one.

You can combine multiple courses in a single course using an import feature. For example, you may want to separate your cluster creation from cluster configuration:

.. code-block:: sh

  touch project/course.yaml
  touch project/gke.yaml
  touch project/init.yaml

And in your `course.yaml` you would import other courses as:

.. code-block:: yaml

  ---
  # project/course.yaml
  - name: Make cluster with gcloud
    import_course: "gke.yaml"

  - name: Configure cluster
    import_course: "init.yaml"

All **imports are relative to the** *course project* **directory**. So for example, if you have two courses that share the same set of tasks, you can put them in e.g. ``includes/`` and import them wherever you need:

.. code-block:: sh

  touch postgres/includes/repo.yaml
  touch postgres/deployment.yaml
  touch postgres/upgrade.yaml

And in one of the courses, you can import the task as:

.. code-block:: yaml

  ---
  # postgres/deployment.yaml
  - name: Update helm repo
    import_course: "includes/repo.yaml"

  # other tasks
  [...]

.. _`Beacons`: beacons.html
