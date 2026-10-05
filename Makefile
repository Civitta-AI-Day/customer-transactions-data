PY := .venv/bin/python

.PHONY: setup seed run test lint format reset

setup:            ## Create the virtualenv, install dependencies, create .env and the database
	@python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else "Python 3.11 or newer is required (python3 is " + sys.version.split()[0] + "). Install it, e.g. brew install python@3.12")'
	python3 -m venv .venv
	$(PY) -m pip install -q --upgrade pip
	$(PY) -m pip install -q -r requirements.txt
	@test -f .env || cp .env.example .env
	$(PY) manage.py migrate
	@echo ""
	@echo "Setup done. Next: make seed"

seed:             ## Fill the database with fake data (about 200,000 transactions)
	$(PY) manage.py seed

run:              ## Start the API on http://127.0.0.1:8000
	$(PY) manage.py runserver

test:             ## Run the test suite
	$(PY) -m pytest

lint:             ## Check code style
	.venv/bin/ruff check .
	.venv/bin/ruff format --check .

format:           ## Fix code style
	.venv/bin/ruff check --fix .
	.venv/bin/ruff format .

reset:            ## Delete the database and seed again from scratch
	rm -f db.sqlite3
	$(PY) manage.py migrate
	$(PY) manage.py seed
