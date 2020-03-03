FROM python:3.8.2-alpine3.11
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app
RUN apk --no-cache add build-base
RUN apk --no-cache add postgresql-dev
RUN pip install -r ./requirements.txt
EXPOSE 8000
