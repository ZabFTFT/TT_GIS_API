FROM python:3.10.8-slim
LABEL maintainer="vlad.zabolotnyi.work@gmail.com"

ENV PYTHONUNBUFFERED 1

WORKDIR app/

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN apt-get update \
    && apt-get install -y \
        binutils \
        libproj-dev \
        gdal-bin

COPY . .

RUN adduser \
    --disabled-password \
    --no-create-home \
    django-user

USER django-user