FROM ubuntu:22.04

# Avoid warnings by switching to noninteractive for the build process
ENV DEBIAN_FRONTEND=noninteractive

ENV USER=root

RUN apt-get update && apt-get install -y git openjdk-18-jre

RUN git clone https://github.com/cdc08x/MINERful.git
WORKDIR MINERful
RUN mkdir /app
RUN mkdir /app/input

ENTRYPOINT ["time","./run-MINERful.sh"]
CMD ["-s","0.9","-c","0.9","iLF","/app/input/bpi2017.xes"]
# docker build -t minerful .
# docker run --rm -d --mount type=bind,source=/home/mavroudopoulos/siesta/SIESTA-BPM-experiments/minerful/input,target=/app/input minerful