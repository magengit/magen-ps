FROM magen_base:17.02
MAINTAINER Alena Lifar

VOLUME ["/opt/server"]
WORKDIR /opt/server
ENV PYTHONPATH $PYTHONPATH:/opt/server

RUN rm -rf __pycache__/

WORKDIR /opt/server/location
RUN rm -rf __pycache__/

WORKDIR /opt/server/location

