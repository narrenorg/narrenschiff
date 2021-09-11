export PIPENV_VENV_IN_PROJECT = 1

PIPENV = pipenv
RUN = $(PIPENV) run
PYTHON = $(RUN) python

.PHONY: pipenv
pipenv:
	$(PIPENV) install --dev

.PHONY: flake8
flake8:
	$(RUN) flake8 .

.PHONY: bandit
bandit:
	$(RUN) bandit -c .bandit.yaml -r narrenschiff/

.PHONY: test
test:
	$(RUN) coverage run -m unittest discover
	$(RUN) coverage report -m
	$(RUN) coverage html

.PHONY: docs
docs:
	$(RUN) sphinx-build -d docs/_build/doctrees/ docs/ docs/_build/html/
	$(RUN) sphinx-build -b coverage docs/ docs/_build/coverage/
	cat docs/_build/coverage/python.txt

.PHONY: clean
clean:
	rm -rf docs/_build

.PHONY: sdist
sdist: pipenv
	$(PYTHON) setup.py sdist
