FROM jfloff/alpine-python:3.6-slim as base

FROM base as builder

RUN pip install --upgrade pip && \
  apk add --update alpine-sdk libxml2-dev libxslt-dev && \
  apk add python3-dev && \
  pip3 install lxml && \
  mkdir /install
# py-pip openssl-dev libffi-dev  zlib-dev 

COPY scripts/install-dronekit.sh /sc/install-dronekit.sh
RUN chmod +x /sc/install-dronekit.sh && /sc/install-dronekit.sh

COPY requirements.txt scripts/install-requirements.sh /sc/
RUN chmod +x /sc/install-requirements.sh && /sc/install-requirements.sh "/sc/requirements.txt"

FROM base
COPY --from=builder /install /usr/local
COPY src /app

WORKDIR /app