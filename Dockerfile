FROM python:3.13

RUN apt-get update && \
    apt-get install -y --no-install-recommends locales \
    libpq-dev \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev && \
    echo "es_ES.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen && \
    rm -rf /var/lib/apt/lists/*

ENV LANG=es_ES.UTF-8
ENV LANGUAGE=es_ES:es
ENV LC_ALL=es_ES.UTF-8

RUN adduser --disabled-password --gecos '' dockuser

WORKDIR /app

COPY pyproject.toml poetry.lock* atlas.hcl /app/

RUN pip install poetry && poetry install --no-root

COPY ./backend/src /app/src
COPY ./backend/db/migrations /app/db/migrations

EXPOSE 8000

# CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["poetry", "run", "fastapi", "run", "src/main.py", "--host", "0.0.0.0", "--port", "8000","--reload"]