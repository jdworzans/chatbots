FROM python:3.9-slim

EXPOSE 8501

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip==22.3.1
COPY streamlit/requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

RUN python -m pip install spacy
RUN python -m spacy download pl_core_news_sm

COPY . .
