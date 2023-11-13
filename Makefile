.PHONY: help prepare-env test lint clean

VENV_NAME?=venv
VENV_ACTIVATE=. $(VENV_NAME)/bin/activate
PYTHON=${VENV_NAME}/bin/python3

.DEFAULT: help
help:
	@echo "make prepare-env"
	@echo "       prepare development environment"
	@echo "make test"
	@echo "       run tests"
	@echo "make lint"
	@echo "       run pylint"

prepare-env:
	python3 -m pip install virtualenv
	make venv

venv: $(VENV_NAME)/bin/activate
$(VENV_NAME)/bin/activate: setup.py
	test -d $(VENV_NAME) || virtualenv -p python3 $(VENV_NAME)
	${PYTHON} -m pip install -U pip setuptools
	${PYTHON} -m pip install -e .  --upgrade --ignore-installed

test: venv
	${PYTHON} -m pytest -s tests

lint: venv
	${PYTHON} -m pylint nisi tests

clean:
	@rm -rf $(VENV_NAME) *.eggs *.egg-info .cache .mypy_cache/ .pytest_cache/
	@rm -rf  *.eggs *.egg-info .cache .mypy_cache/ .pytest_cache/
