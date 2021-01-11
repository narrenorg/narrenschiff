``.narrenschiff.yaml``
======================

Every project needs to contain ``.narrenschiff.yaml`` configuration file. This file is used to point to password, and salt files, as well as to define the cluster context. This file should be commited to the source control of your project.

.. code-block:: yaml

  # Example of configuration file
  key: ./password.txt  # path to file containing password for encrypting files
  spice: ./salt.txt  # path to file containing salt (salt should be random and long)

  # If you are managing multiple clusters, your project may be tied to one
  # particular cluster. Instead of switching context manually with:
  #
  #   kubectl config use-context CONTEXT_NAME
  #
  # you can define context in this section of your project configuration file.
  # If you are not sure which context you are using, check it with:
  #
  #   kubectl config get-contexts
  #
  # or:
  #
  #   kubectl config current-context
  #
  # context.name is the name of the context [default: undefined]
  # context.use defines whether to use context switching before executing tasks
  #   value is boolean or quoted boolean string [default: "false"]
  context:
    name: cloud_provider_project_id_region_zone_project_title
    use: "false"
