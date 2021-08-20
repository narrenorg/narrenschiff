# Narrenschiff

[![Documentation Status](https://readthedocs.org/projects/narrenschiff/badge/?version=latest)](https://docs.narrenschiff.xyz/en/latest/?badge=latest)

> Imagine then a fleet or a ship in which there is a captain who is taller and stronger than any of the crew, but he is a little deaf and has a similar infirmity in sight, and his knowledge of navigation is not much better. The sailors are quarreling with one another about the steering––every one is of the opinion that he has a right to steer, though he has never learned the art of navigation and cannot tell who taught him or when he learned, and will further assert that it cannot be taught, and they are ready to cut in pieces any one who says the contrary. They throng about the captain, begging and praying him to commit the helm to them; and if at any time they do not prevail, but others are preferred to them, they kill the others or throw them overboard, and having first chained up the noble captain's senses with drink or some narcotic drug, they mutiny and take possession of the ship and make free with the stores; thus, eating and drinking, they proceed on their voyage in such a manner as might be expected of them. Him who is their partisan and cleverly aids them in their plot for getting the ship out of the captain's hands into their own whether by force or persuasion, they compliment with the name of sailor, pilot, able seaman, and abuse the other sort of man, whom they call a good-for-nothing; but that the true pilot must pay attention to the year and seasons and sky and stars and winds, and whatever else belongs to his art, if he intends to be really qualified for the command of a ship, and that he must and will be the steerer, whether other people like or not––the possibility of this union of authority with the steerer's art has never seriously entered into their thoughts or been made part of their calling. Now in vessels which are in a state of mutiny and by sailors who are mutineers, how will the true pilot be regarded? Will he not be called by them a prater, a star-gazer, a good-for-nothing?
> Plato, Republic

Ansible-like configuration management tool for the Kubernetes.

## Quickstart

### Requirements

* Python 3.6 or higher
* `kubectl` v1.20 or higher
* `helm` v3.0 or higher
* `gcloud` 343.0.0 or higher

### Installation

You can easily install it with `pip`:

```
pip install narrenschiff
```

We advise you to install it in virtualenv.

### Quickstart

To install Narrenschiff in virtualenv execute:

```
$ mkdir infrastructure && cd infrastructure
$ git init
$ python3 -m venv env  && echo 'env' > .gitignore
$ . env/bin/activate
$ pip install narrenschiff
```

Initialize a course project, and encrypt a treasure:

```
$ narrenschiff dock --autogenerate --location postgres/
$ narrenschiff chest stash --treasure postgresPassword --value "Password123!" --location postgres/
```

Create a template for `Secret` Kubernetes resource, using encrypted treasure:

```
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
```

Create a course:

```
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
```

Deploy:

```
$ narrenschiff sail --set-course postgres/course.yaml
```

That's it! Secret is now deployed to your cluster. Head over to [General Overview][1] to get familiar with Narrenschiff terminology, or to [Getting Started][2] to learn how to make your first project.

### Acknowledgements

I want to personally give thanks to [brainshuttle LLC][3], the company I've worked for years. If it wasn't for their creative atmosphere, and enthusiasm to give space to new ideas, this project would not come to fruition.

[1]: https://docs.narrenschiff.xyz/en/latest/narrenschiff/overview.html
[2]: https://docs.narrenschiff.xyz/en/latest/narrenschiff/getting_started.html
[3]: https://brainshuttle.com/
