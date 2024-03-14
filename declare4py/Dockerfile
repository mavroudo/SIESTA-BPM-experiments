FROM python:3.11-slim-bullseye
LABEL authors="mavroudo"
RUN pip install --upgrade pip
RUN mkdir "/app"
RUN mkdir "/app/dataset"
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY src/ /app/src
COPY evaluation/ /app/evaluation
#COPY data_1000.xes /app/dataset/data_1000.xes

# Command: docker run -v dataset:/app/dataset extract_logs params
ENTRYPOINT ["python", "-m", "evaluation.evalaute"]
#ENTRYPOINT ["python", "script.py"]