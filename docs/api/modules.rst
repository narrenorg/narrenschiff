Modules
=======

Modules are way of implementing CLI commands e.g. ``kubectl``. ``narrenschiff`` can be extended with new modules. All modules should reside in ``narrenschiff.modules`` package.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules/common
   modules/kubectl
   modules/kustomization
   modules/helm
   modules/gcloud
   modules/wait_for_pod
