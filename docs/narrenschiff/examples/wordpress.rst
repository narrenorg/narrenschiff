Deploying WordPress and MySQL with Persistent Volumes
=====================================================

This examples is taken from the official Kubernetes documentation_ which is licensed under `CC BY 4.0`_. The example will be addapted to fit deployment process in Narrenschiff.

Before you Start
----------------

We advise you to use Minikube as you follow along this tutorial. Minikube is easy to setup, and manage. See the installation process in the `official documentation`_, or see our `getting started`_ tutorial.

You can find the source code for this tutorial in the official Narrenschiff repo_ under the `examples/` directory. The example in the repo uses ``.narrenschiff.yaml`` configuration from the repo itself. But, for completes purposes, we will show how to properly start a project.

Start the Project
-----------------

Start by installing Narrenschiff and making a project.

.. code-block:: sh

  $ mkdir wordpress && cd wordpress
  $ git init
  $ python3 -m venv env  && echo 'env' >> .gitignore
  $ . env/bin/activate
  $ pip install narrenschiff

Now you are ready to make a course project. In the root project, execute following command:

.. code-block:: sh

  $ narrenschiff dock --autogenerate --location wordpress

Stash Your Treasure in a Chest
------------------------------

We need a password for MySQL and wel'll start by stashing the password in the chest.

.. code-block:: sh

  $ narrenschiff chest stash --treasure 'mysql_password' --value 'Password123!' --location wordpress/

In the next section we'll add Kubernetes resources to our project.

Add Resource Configuration for MySQL and Wordpress
--------------------------------------------------

We'll add MySQL password to the template for the Secret. Place the template under ``wordpress/files/mysql/secret.yaml``:

.. code-block:: yaml

  # wordpress/files/mysql/secret.yaml
  ---
  apiVersion: v1
  kind: Secret
  type: Opaque
  metadata:
    name: mysql-pass
  data:
    MYSQL_ROOT_PASSWORD: "{{ mysql_password | b64enc }}"

Remember, ``files/`` is reserved in a course project for templates. All templates are referenced in courses relative to this directory.

Make the following files in ``wordpress/files/mysql`` (filenames are in the comments):

.. code-block:: yaml

  # wordpress/files/mysql/service.yaml
  ---
  apiVersion: v1
  kind: Service
  metadata:
    name: wordpress-mysql
    labels:
      app: wordpress
  spec:
    ports:
      - port: 3306
    selector:
      app: wordpress
      tier: mysql
    clusterIP: None

  # wordpress/files/mysql/pvc.yaml
  ---
  apiVersion: v1
  kind: PersistentVolumeClaim
  metadata:
    name: mysql-pv-claim
    labels:
      app: wordpress
  spec:
    accessModes:
      - ReadWriteOnce
    resources:
      requests:
        storage: 50Mi

  # wordpress/files/mysql/deployment.yaml
  ---
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: wordpress-mysql
    labels:
      app: wordpress
  spec:
    selector:
      matchLabels:
        app: wordpress
        tier: mysql
    strategy:
      type: Recreate
    template:
      metadata:
        labels:
          app: wordpress
          tier: mysql
      spec:
        containers:
        - image: mysql:5.6
          name: mysql
          envFrom:
            - secretRef:
                name: mysql-pass
          ports:
          - containerPort: 3306
            name: mysql
          volumeMounts:
          - name: mysql-persistent-storage
            mountPath: /var/lib/mysql
        volumes:
        - name: mysql-persistent-storage
          persistentVolumeClaim:
            claimName: mysql-pv-claim

These were all simple manifests. We didn't have any need to use templating here. But the neat thing about Narrenschiff is that you can add templating to whatever manifest you need whenever you need it. We will now proceed to write manifests for the Wordpress itself:

.. code-block:: yaml

  # wordpress/files/wordpress/secret.yaml
  ---
  apiVersion: v1
  kind: Secret
  type: Opaque
  metadata:
    name: wordpress-env
  data:
    WORDPRESS_DB_PASSWORD: "{{ mysql_password | b64enc }}"

  # wordpress/files/wordpress/service.yaml
  ---
  apiVersion: v1
  kind: Service
  metadata:
    name: wordpress
    labels:
      app: wordpress
  spec:
    ports:
      - port: 80
    selector:
      app: wordpress
      tier: frontend
    type: LoadBalancer

  # wordpress/files/wordpress/pvc.yaml
  ---
  apiVersion: v1
  kind: PersistentVolumeClaim
  metadata:
    name: wp-pv-claim
    labels:
      app: wordpress
  spec:
    accessModes:
      - ReadWriteOnce
    resources:
      requests:
        storage: 100Mi

  # wordpress/files/wordpress/deployment.yaml
  ---
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: wordpress
    labels:
      app: wordpress
  spec:
    selector:
      matchLabels:
        app: wordpress
        tier: frontend
    strategy:
      type: Recreate
    template:
      metadata:
        labels:
          app: wordpress
          tier: frontend
      spec:
        containers:
        - image: wordpress:5.5-apache
          name: wordpress
          env:
          - name: WORDPRESS_DB_HOST
            value: wordpress-mysql
          envFrom:
            - secretRef:
                name: wordpress-env
          ports:
          - containerPort: 80
            name: wordpress
          volumeMounts:
          - name: wordpress-persistent-storage
            mountPath: /var/www/html
        volumes:
        - name: wordpress-persistent-storage
          persistentVolumeClaim:
            claimName: wp-pv-claim

Deploy
------

Before deployment, we have to write the course:

.. code-block:: yaml

  # wordpress/course.yaml
  ---
  - name: Deploy Mysql
    kubectl:
      command: apply
      args:
        filename:
          - mysql

  - name: Deploy Wordpress
    kubectl:
      command: apply
      args:
        filename:
          - wordpress

Finally apply your changes to the cluster:

.. code-block:: sh

  $ narrenschiff sail --set-course wordpress/course.yaml

You can verify that wordpress is deployed by accessing it through your browser to finish the installation:

.. code-block:: sh

  $ minikube service wordpress --url

Copy and paste the URL to your browser, and you can complete the wordpress intallation. Use ``minikube stop && minikube delete`` to stop and delete the cluster.

Verify
------

.. _documentation: https://kubernetes.io/docs/tutorials/stateful-application/mysql-wordpress-persistent-volume/
.. _`CC BY 4.0`: https://creativecommons.org/licenses/by/4.0/deed.ast
.. _`official documentation`: https://kubernetes.io/docs/tasks/tools/install-minikube/
.. _`getting started`: ../getting_started.html
.. _repo: https://github.com/petarGitNik/narrenschiff
