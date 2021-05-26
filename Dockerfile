FROM python:3.8-buster

WORKDIR /app

# Copy pip requirements
COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt --no-cache

CMD