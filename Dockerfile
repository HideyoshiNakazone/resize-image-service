FROM python:3.12

WORKDIR /app

RUN pip install poetry

COPY ./ /app/

RUN poetry install

ENTRYPOINT ["poetry", "run", "python", "-m", "storage_service"]
