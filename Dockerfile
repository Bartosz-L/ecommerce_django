FROM python:3.8.1-alpine3.11
LABEL maintainer="Bartosz Ligęza"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONIOENCODING=utf-8
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV PORT=8000

RUN mkdir /app
WORKDIR /app

COPY ./requirements.txt /app/

# Install build dependencies
RUN apk update \
    && apk add --no-cache --virtual .build-deps gcc musl-dev gettext \
    && apk add jpeg-dev zlib-dev libjpeg cairo-dev pango-dev gdk-pixbuf

# Install project dependencies
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

# Delete build dependencies
RUN apk del .build-deps

COPY . /app/

RUN adduser -D user
RUN chown -R user:user .
USER user