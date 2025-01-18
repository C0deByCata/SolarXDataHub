PYTHON_FILES := $(shell find solarxdatahub -name '*.py')

ENV := poetry
PYTHON := $(ENV) run python3

.PHONY: install_env install_dev_env clean lint format check_format run

# Installing environment
install_env:
	$(ENV) install --no-dev

install_dev_env:
	$(ENV) install

# Code
lint:
	$(ENV) run python3 -m pylint $(PYTHON_FILES)

format:
	$(ENV) run poetry run ruff check --fix $(PYTHON_FILES)

check_format:
	$(ENV) run poetry run ruff check $(PYTHON_FILES)

run:
	$(PYTHON) -m solarxdatahub
