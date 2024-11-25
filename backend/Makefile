.ONESHELL:

.PHONY: clean install tests run all

clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete
	find . -type d -name '__pycache__' -delete
	rm .venv -rf

install:
	python3 -m venv .venv; \
	. .venv/bin/activate; \
	pip install -r requirements.txt --no-cache-dir;

run:
	mkdir logs; \
	. .venv/bin/activate; \
	export FLASK_APP=flasky.py; \
	flask run

all: clean install run
