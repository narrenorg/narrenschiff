flake8:
	pipenv run flake8 .

test:
	pipenv run coverage run -m unittest discover
	pipenv run coverage report -m
	pipenv run coverage html
