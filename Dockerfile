FROM python:3.13.0-alpine
LABEL maintainer="posseydon87@gmail.com"

ENV PYTHONBUFERRED 1

WORKDIR app/

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
