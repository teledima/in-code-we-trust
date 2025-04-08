FROM python:3.12-alpine

WORKDIR /in-code-we-trust

COPY pyproject.toml poetry.lock ./
COPY app/ ./app/
COPY settings.toml config.py run.py ./

RUN pip install --no-cache-dir poetry && \
 poetry config virtualenvs.create false && \
 poetry install --no-interaction --only main

EXPOSE 8000

CMD ["python", "run.py"]
