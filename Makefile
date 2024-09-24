format:
	python -m black -S --line-length 79 --preview ./
	isort ./

lint:
	flake8 ./app
	flake8 ./run.py

type:
	python -m mypy --no-implicit-reexport --ignore-missing-imports --no-namespace-packages ./

ci: format lint type