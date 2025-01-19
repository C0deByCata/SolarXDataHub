FROM python:3.11-slim-buster

# Configurar la zona horaria
ENV TZ=Europe/Madrid
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Instalar Poetry
RUN pip install poetry==2.0.1

# Variables de entorno para Poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /usr/solarxdatahub

COPY pyproject.toml poetry.lock ./

RUN poetry install --without dev --no-root

COPY . .

CMD ["python", "-m", "solarxdatahub"]
