FROM python:3.10-slim

WORKDIR /app

COPY poetry.lock pyproject.toml /code/

RUN pip install poetry

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

COPY . /app/

EXPOSE 8000

# Start FastAPI
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
