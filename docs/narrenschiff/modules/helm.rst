helm
====

Description
-----------

Execute ``helm`` commands. Deploy, upgrade, and delete your charts.

Requirements
------------

* ``kubectl``
* ``helm``

Parameters
----------

.. list-table::
  :header-rows: 1

  * - Parameter
    - Comment
  * - command
    - Any helm command with nested subcommands
  * - args
    - flag/value pairs, a flag needs to be listed by its full name
  * - opts
    - flags without arguments i.e. switches
  * - chart
    - name of the chart
  * - name
    - name of the chart release

Examples
--------

.. code-block:: yaml

  # If you have a simple command with an argument you can write it like this
  # helm repo add stable https://kubernetes-charts.storage.googleapis.com/
  - name: Add stable repo to Helm
    helm:
      command: repo add stable https://kubernetes-charts.storage.googleapis.com/

  # Command (repo) and its subcommand (update) are both placed in the "command"
  # parameter of Narrenschiff helm module
  # helm repo update
  - name: Update repo for stable charts
    helm:
      command: repo update

  # use "chart" and "name" to define chart and its release
  # helm install ingress-controller stable/nginx-ingress --atomic --namespace default
  - name: Install Ingress controller
    helm:
      command: install
      name: ingress-controller  # release of the chart
      chart: stable/nginx-ingress  # chart you're using from the chart repo
      opts:  # all switches are listed in opts as YAML list
        - atomic
      args:  # all flags with inputs go under args
        namespace: default
        version: 1.41.1

  # You can use "set" to set values on the command line
  - name: Install cert-manager
    helm:
      command: install
      name: cert-manager
      chart: jetstack/cert-manager
      opts:
        - atomic
      args:
        namespace: cert-manager
        version: v0.12.0
        set:  # set is a YAML list of key/value pairs
          - ingressShim.defaultIssuerName=letsencrypt-prod
          - ingressShim.defaultIssuerKind=ClusterIssuer
          - ingressShim.defaultIssuerGroup=cert-manager.io

  # In Narrenschiff you can combine "set" with templating if you need to set some secrets
  - name: Install PostgreSQL
    helm:
      command: install
      name: postgres
      chart: bitnami/postgresql
      opts:
        - atomic
      args:
        version: 9.1.1
        set:
          - "global.postgresql.postgresqlPassword={{ postgresqlPassword }}"

  # Values can be used when you have URLs as your chart values
  - name: Upgrade Chart Museum
    helm:
      command: upgrade
      name: museum
      chart: stable/chartmuseum
      opts:
        - atomic
        - cleanup-on-fail
      args:
        version: 2.13.0
        values:
          - https://github.com/helm/charts/blob/master/stable/chartmuseum/values.yaml

  # Files in "values" are always passed as secretmaps!
  - name: Install Graylog
    helm:
      command: install
      name: "graylog"
      chart: stable/graylog
      opts:
        - atomic
      args:
        namespace: "graylog"
        version: 1.6.9
        values:
          - "{{ ingress | secretmap }}"
          - "{{ service | secretmap }}"

Status
------

.. warning::

  This module is experimental.
