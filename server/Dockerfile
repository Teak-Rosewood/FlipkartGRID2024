FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN pip install poetry qdrant-client[fastembed]

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

COPY . /app/

EXPOSE 8000

# Start FastAPI
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
