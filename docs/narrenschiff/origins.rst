More than a satire, a tool!
===========================

So, what's your selling point?
------------------------------

Encrypted secrets (strings) and files.

What's up with all the funky terminology?
-----------------------------------------

Why is it that some of the biggest **cloud** tools (Docker, Kubernetes, Helm) out there are named using **ocean** related references? Heck, there's even a cloud provider having ocean_ in its name.

So I decided to make both a tool, and a satire. Therefore, I needed a name that will be in the spirit of the cloud, i.e. related to seas, and oceans of course. And also a name that would describe the current state of DevOps. Narrenschiff_ (ship of fools) was the only logical choice.

I also find multitude of terminology `amusing` (to say the least): Ansible calls its YAML files playbooks, and vars files, Kubernetes calls its YAML files manifests, and Helm calls bundled templated YAML files – charts.

And why does everything has to have its own terminology or domain specific language? Didn't we have enough of the `tool fatigue`_? To cite one GitHub user:

  "The concept of tool fatigue is real -- the k8s operation space is already crowded as it is, don't make people learn `extra` tools unless there's a really good reason, and this does not seem like one…" jshearer_

I fully and unironiracally agree with **jshearer**! Thefore I decided to go even a step further! Not only will I call YAML files by a special name, I will call them by many names: courses, chests, secretmaps, vars. Heck, passwords and salts? Pfff… That’s yesterdays story: they are now keys and spices. No more boring old terminology we all got used to! `Stash` your secrets in a chest (don’t just say “I’m `encrypting` them”), or `loot` a ``--treasure`` from the chest (saying “decrypting a secret” is for boomers). Deployment? Nah, board the ``narrenschiff``, ``--set-course``, and ``sail``.

We already have ``secretGenerator`` option in kustomize. Why should we use Narrenschiff?
----------------------------------------------------------------------------------------

Since we all have a tool lock-in with Kubernetes you might as well use all the available options the tool gives you.

That being said, it is really easy to encrypt ``values.yaml`` if it contains secrets, or to template your Manifests, with Narrenschiff. You can even use ``secretGenerator`` with Narrenschiff.

Although I consider the encrypted strings and files to be the most powerful features of Narrenschiff, it's also a "procedural/declerative task executor" or whatever you want to call it (it's **YAML instead of** a **bash** script - come to think of it, we should also have an acronym for that - YIOB - it just rolls off the tongue). So this is one more reason to use it. It's a Kubernetes configuration management tool for small business that were insanse enough to start with Kubernetes in the first place.

Ansible has Kubernetes module, and it is a mature tool, why should we choose Narrenschiff over it?
--------------------------------------------------------------------------------------------------

Yes. In general. When I had to make the decision on how to manage the cluster the most important thing for me was to encrypt secrets and push them to the repo. I also wanted to encrypt certificates for Helm Tiller (since Tiller still existed at that point) and source commit them without leaking content. And configuration management (preparation of the cluster, and management later) was a must. Ansible was almost a natural choice, since there wasn't anything similar at the time (at least to my knowledge).

And yes, it has both the Kubernetes and the GCP module. However, when I tried the most basic of basic commands, for listing inventories, it failed. Keep in mind, this was just a first step to do when using the damn plugin. I submitted the `bug report`_ and it was actually fixed_ two days later, however, I didn't want to bother with it anymore, since most basic configuration was failing. And, the thing I found confusing (and not pleasing) was pasting of the whole Kubernetes manifests inside playbooks, or using awkward syntax for template lookup.

Ansible is great tool and battle tested. Narrenschiff at this point is still in beta. The choice is clear... (choose a tool in beta of course! - we always need to be on a bleeding edge and work with more and more tools, and new technologies, r-right?)

And also... I wanted to build my own tool.

But why?
--------

It's just a tool bro.

.. _ocean: https://www.digitalocean.com/
.. _Narrenschiff: https://en.wikipedia.org/wiki/Ship_of_fools
.. _`tool fatigue`: https://landscape.cncf.io/
.. _jshearer: https://github.com/kubernetes-sigs/kustomize/issues/119#issuecomment-515787267
.. _`bug report`: https://github.com/ansible/ansible/issues/60584
.. _fixed: https://github.com/ansible/ansible/pull/60603
