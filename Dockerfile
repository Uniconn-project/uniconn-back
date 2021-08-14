FROM python:3.9-alpine

WORKDIR /code

RUN pip install --upgrade pip

RUN apk update \
    && apk add gcc postgresql-dev python3-dev musl-dev \
    && apk add zlib libjpeg-turbo-dev libpng-dev freetype-dev lcms2-dev libwebp-dev harfbuzz-dev fribidi-dev tcl-dev tk-dev

COPY requirements.txt /code/

RUN pip install -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /code/
