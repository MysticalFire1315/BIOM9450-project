.ONESHELL:

.PHONY: clean install tests run all

clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete

install:
	python3 -m .venv; \
	. .venv/bin/activate; \
	pip install -r requirements.txt;

tests:
	. .venv/bin/activate; \
	export FLASK_APP=flasky.py; \
	flask test

run:
	. .venv/bin/activate; \
	export FLASK_APP=flasky.py; \
	flask run

all: clean install tests run
