FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

LABEL mantainer="Borja Lopez"

ARG USER=fastapi

ENV APP_MODULE="main:app" \
    WORKERS_PER_CORE=2 \
    PORT=80 \
    HOST=0.0.0.0 \
    LOG_LEVEL=info


RUN useradd -m -b /app --shell /bin/bash --uid 1000 ${USER}

COPY ./requirements.txt /app/requirements.txt

RUN python -m pip install --upgrade pip --no-cache-dir && \
    pip install --no-cache-dir -r /app/requirements.txt

COPY --chown=1000 ./src /app

USER ${USER}
