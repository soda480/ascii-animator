ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim AS build-image

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /code
COPY . /code/

RUN apt-get update && \
    apt-get install -y --no-install-recommends make && \
    rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip && \
    pip install -e .[dev] && \
    make build


FROM python:${PYTHON_VERSION}-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /opt/ascii-animator

COPY --from=build-image /code/dist/ascii-animator-*.tar.gz /opt/ascii-animator
COPY --from=build-image /code/docs/examples /opt/ascii-animator/examples

RUN pip install faker ascii-animator-*.tar.gz