.PHONY: clean clean-docs clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test clean-docs ## remove all build, test, coverage, Python artifacts and docs

clean-docs:
	rm -fr docs/_build

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -f .coverage.*
	rm -fr htmlcov/
	rm -fr .pytest_cache
	-rm -rf .test*
	-rm -rf .mypy_cache

lint: ## check style with flake8
	flake8 zlmdb tests

test-single:
	clear && pytest -v -s zlmdb/tests/test_basic.py

test-quick:
	pytest

test:
	tox -e py36,flake8,coverage,mypy,yapf,sphinx

test-all:
	tox

coverage: ## check code coverage quickly with the default Python
	#coverage run --source zlmdb -m pytest
	coverage run --source zlmdb --omit="zlmdb/flatbuffer/reflection/*,zlmdb/flatbuffer/demo/*,zlmdb/tests/*" -m pytest -v -s zlmdb
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	sphinx-build -b html ./docs ./docs/_build
	$(BROWSER) docs/_build/index.html

dist: clean ## builds source and wheel package
	python setup.py sdist bdist_wheel
	ls -la dist

# publish to PyPI
publish: dist
	twine upload dist/*

install:
	pip install -e .
	pip install -r requirements-dev.txt

flatbuffers:
	~/scm/3rdparty/flatbuffers/flatc --python -o zlmdb/flatbuffer/ zlmdb/flatbuffer/demo.fbs
	~/scm/3rdparty/flatbuffers/flatc --python -o zlmdb/flatbuffer/ zlmdb/flatbuffer/reflection.fbs

# auto-format code - WARNING: this my change files, in-place!
autoformat:
	yapf -ri --style=yapf.ini --exclude="zlmdb/flatbuffer/*" zlmdb
