ARG PYTHON_VERSION=3.11.1
FROM python:${PYTHON_VERSION}-buster as builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

ENV POETRY_VERSION=1.7.1
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN pip install poetry==${POETRY_VERSION}

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --only main --no-ansi --no-root && rm -rf $POETRY_CACHE_DIR


FROM python:${PYTHON_VERSION}-slim-buster as runner

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY core ./app/core
COPY user ./app/user
COPY manage.py ./app/manage.py
COPY gunicorn.conf.py ./app/gunicorn.conf.py
COPY entrypoint.sh ./app/entrypoint.sh

WORKDIR /app

RUN chmod +x entrypoint.sh
RUN python manage.py collectstatic --no-input

EXPOSE 8000

CMD ./entrypoint.sh
