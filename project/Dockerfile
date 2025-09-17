FROM python:3.12-slim


RUN apt-get update && \
    pip install --upgrade pip && \
    pip install django djangorestframework djangorestframework-simplejwt \
    psycopg2-binary PyPDF2 openai qdrant-client  sentence_transformers ; \
    apt-get install -y postgresql-client

WORKDIR /backend

RUN pip freeze > requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
