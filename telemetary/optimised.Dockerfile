FROM jfloff/alpine-python:3.6-slim as base

RUN apk update
FROM base as builder

RUN pip install --upgrade pip

RUN apk update && \
  apk add --virtual build-dependencies build-base gcc wget git && \
  apk add --update libxml2-dev libxslt-dev

RUN apk add python3-dev && \
  pip3 install lxml && \
  mkdir /install
# py-pip openssl-dev libffi-dev  zlib-dev 

COPY scripts/install-dronekit.sh /sc/install-dronekit.sh
RUN chmod +x /sc/install-dronekit.sh && /sc/install-dronekit.sh

COPY requirements.txt scripts/install-requirements.sh /sc/
RUN chmod +x /sc/install-requirements.sh && /sc/install-requirements.sh "/sc/requirements.txt"
# RUN apk del build-dependencies build-base gcc wget git libxml2-dev libxslt-dev
# RUN apk del build-dependencies build-base gcc wget git

FROM base
COPY --from=builder /install /usr/local/lib/python3.6

WORKDIR /app
CMD [ "python3",  "main.py"]