FROM python:3.8-slim-bullseye
LABEL authors="mavroudo"
RUN pip install --upgrade pip
RUN pip install pandas pm4py==2.7.10.3

RUN mkdir "/app"
RUN mkdir "/app/dataset"
WORKDIR /app
COPY extract_logs.py /app/script.py

# Command: docker run -v dataset:/app/dataset extract_logs params

ENTRYPOINT ["python", "script.py"]