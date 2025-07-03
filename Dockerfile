FROM python:3.13

RUN adduser --disabled-password --gecos '' dockuser

WORKDIR /app

COPY pyproject.toml poetry.lock* atlas.hcl /app/

RUN pip install poetry && poetry install --no-root

COPY ./src /app/src
COPY ./db/migrations /app/db/migrations

# NO cambies a dockuser aquí, deja que todo corra como root
# USER dockuser

EXPOSE 8000

# CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["poetry", "run", "fastapi", "run", "src/main.py", "--host", "0.0.0.0", "--port", "8000"]