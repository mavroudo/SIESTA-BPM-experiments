FROM ubuntu:22.04

# Avoid warnings by switching to noninteractive for the build process
ENV DEBIAN_FRONTEND=noninteractive

ENV USER=root

RUN apt-get update && apt-get install -y git openjdk-18-jre time

RUN git clone https://github.com/cdc08x/MINERful.git
WORKDIR MINERful
RUN mkdir /app
RUN mkdir /app/input

# Change the given memory to 50GB
RUN sed -i 's/MEMORY_MAX="8096m"/MEMORY_MAX="50g"/g' run-MINERful.sh


ENTRYPOINT ["time","./run-MINERful.sh"]
CMD ["-s","0","-c","0","-iLF","/app/input/log.xes","-prune","none"]
# docker build -t minerful .
# docker run --rm --mount type=bind,source=/home/balaktsis/experiments/,target=/app/input minerful