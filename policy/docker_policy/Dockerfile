FROM 079349112641.dkr.ecr.us-west-2.amazonaws.com/magen-core:latest
MAINTAINER Alena Lifar

VOLUME ["/opt/server"]
WORKDIR /opt/server
ENV PYTHONPATH $PYTHONPATH:/opt/server:/opt/server/policy:/opt/server/policy/policy_server

RUN rm -rf __pycache__/
RUN rm -rf tests/__pycache__/

WORKDIR /opt/server/policy

RUN rm -rf __pycache__/
RUN rm -rf tests/__pycache__/

# For production:
# RUN pip3 install magen-policy-service

# For dev:
WORKDIR /tmp
COPY magen_location_service-1.0a2-py3-none-any.whl /tmp
RUN pip3 install magen_location_service-1.0a2-py3-none-any.whl
COPY magen_policy_service-1.0a1-py3-none-any.whl /tmp
RUN pip3 install magen_policy_service-1.0a1-py3-none-any.whl

WORKDIR /opt/server/policy
