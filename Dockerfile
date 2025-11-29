FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip \
  && pip install poetry

WORKDIR /usr/src/app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --no-interaction

COPY src/ ./src/

# Entrypoint: start main.py using poetry
ENTRYPOINT ["poetry", "run", "python", "src/main.py"]

