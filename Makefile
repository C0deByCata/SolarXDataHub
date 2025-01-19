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

#Docker
#Create docker image
docker_build:
	docker build -t solarxdatahub .

#up the service
docker_up:
	docker-compose up -d

#down the service
docker_down:
	docker-compose down

# view logs
docker_logs:
	docker-compose logs -f

# run docker image removing it after
docker_run_rm:
	docker run --rm solarxdatahub

# run docker image
docker_run:
	docker run --name solarxdatahub_app solarxdatahub
