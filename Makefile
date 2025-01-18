PYTHON_FILES := $(shell find solarxdatahub -name '*.py')

ENV := poetry
PYTHON := $(ENV) run python3

# Installing environment
install_env:
	$(ENV) install --no-dev

install_dev_env:
	$(ENV) install

# Code
lint:
	$(PYTHON) -m pylint $(PYTHON_FILES)

format:
	$(PYTHON) run ruff check --fix $(PYTHON_FILES)

check_format:
	$(PYTHON) run ruff check $(PYTHON_FILES)

run:
	$(PYTHON) -m solarxdatahub