FROM python:3.9.0-slim

ENV USER=dashboard

LABEL maintainer="Borja Lopez"

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Create a non-root user group
RUN useradd \
      --uid 1000 \
      --shell /bin/bash \
      -d /app \
      -m \
      ${USER}

WORKDIR /app

RUN apt-get update && \
        apt-get install -y wkhtmltopdf --no-install-recommends && \
        apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app

RUN pip install --upgrade pip --no-cache-dir && \
    pip install -r /app/requirements.txt --no-cache-dir

COPY ./src /app

USER ${USER}

COPY --chown=${USER} start.sh /app/start.sh

CMD ["/app/start.sh"]
