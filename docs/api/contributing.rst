Contributing
============

Setup development environment
-----------------------------

If you decide to contribute to the code base, you'll first have to fork the project on GitHub, and then clone the project in the local environment. You'll need a GitHub account in order to make a fork.

Make a clone of the repository, and install dependencies (just replace `<your_github_username>` with your actual GitHub username). This project is currently using ``pipenv`` to manage its dependencies. This could be changed in the future.

.. code-block:: sh

    git clone https://github.com/<your_github_username>/narrenschiff.git
    pipenv install --dev

This project is using ``unittest`` framework form the Python standard library. After you clone the repo, you can run tests to make sure everything is working:

.. code-block:: sh

    make test

If you want to contribute to documentation, you can build it locally:

.. code-block:: sh

    cd docs/
    make html

Now that you have the development environment all setup, it's best to make a new branch for your feature (or bug fix!), and make changes there:

.. code-block:: sh

    git checkout -b my-new-feature

When you finish coding, use ``make test`` to test the changes. If all is good, push the branch to your fork, and make a pull request. Don't forget to add unit tests for the new feature.

Keeping your fork synced with upstream
--------------------------------------

If you followed the previously described setup, then you can easily keep your fork up-to-date with the original repository. First, you need to add the upstream repository to your project:

.. code-block:: sh

    git remote add upstream https://github.com/narrenorg/narrenschiff.git

Then, you can fetch changes made to the master, and push them to your fork:

.. code-block:: sh

    git fetch upstream
    git merge upstream/master
    git push origin master

Coding Style
------------

This project is mainly styled according to PEP8. Please use ``flake8`` to check the style of your code before making a pull request. This project comes with `.flake8` configuration file.
