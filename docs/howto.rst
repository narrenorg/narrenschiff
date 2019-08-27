Starting a project
==================

Start managing your infrastructure by first laying out a directory structure:

.. code-block:: sh

  mkdir infrastructure
  cd infrastructure
  git init
  mkdir project
  touch project/course.yaml
  touch project/vars.yaml
  touch project/chest.yaml
  touch project/secretmap.yaml
  touch .narrenschiff.yaml

Then generate key and spice, and put it somewhere other than your git managed project:

.. code-block:: sh

  mkdir ~/.infrastructure
  head -c 30 /dev/urandom | base64 > password.txt
  head -c 30 /dev/urandom | base64 > salt.txt

After that, you're ready to start writing your courses. You can chunk out your course files using the import feature. For example, you may want to separate your cluster creation from cluster configuration:

.. code-block:: sh

  touch project/course.yaml
  touch project/gke.yaml
  touch project/init.yaml

And in your `course.yaml` import other courses:

.. code-block:: yaml

  ---
  # course.yaml
  - name: Make cluster with gcloud
    import_course: "gke.yaml"

  - name: Configure cluster
    import_course: "init.yaml"
