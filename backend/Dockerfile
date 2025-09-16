FROM python:3.12-slim


# RUN apt-get update && apt-get install -y python3 python3-dev python3-pip build-essential libblas-dev liblapack-dev libatlas-base-dev
RUN apt-get update && \
    pip install --upgrade pip && \
    pip install django djangorestframework djangorestframework-simplejwt \
    psycopg2-binary PyPDF2 openai qdrant-client  sentence_transformers
        
    # python-dotenv    python-multipart  redis celery

WORKDIR /backend

RUN pip freeze > requirements.txt

# RUN pip install -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# COPY manage.py .
# RUN python3 manage.py migrate
# how to write in cmd two command lines

# CMD [ "python3", "manage.py", "f" ]

CMD [ "tail", "-f" ]