FROM python:3.11-slim

WORKDIR /backend

ENV PYTHONPATH=/backend

ENV PYTHONDONTWRITEBYTECODE=1

# First copy only requirements.txt to cache dependencies independently
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /backend

RUN chmod +x /backend/pre-start.sh


EXPOSE 80

