FROM python:3.9-slim

EXPOSE 8501

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

COPY app.py /app/app.py

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=80", "--server.address=0.0.0.0"]
