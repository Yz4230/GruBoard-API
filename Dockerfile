FROM python:3.8-alpine3.11
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY ./reqs.txt /app
RUN apk --no-cache add build-base
RUN apk --no-cache add postgresql-dev
RUN pip install -r ./reqs.txt
EXPOSE 8000
