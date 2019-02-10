FROM jfloff/alpine-python:3.6-slim

RUN pip install --upgrade pip

RUN apk update && \
  apk add --virtual build-dependencies build-base gcc wget git && \
  apk add --update libxml2-dev libxslt-dev

RUN apk add python3-dev && \
  pip3 install lxml && \
  mkdir /install
# py-pip openssl-dev libffi-dev  zlib-dev

RUN sed -i 's/, int,/, unsigned int,/' /usr/include/assert.h && \
  git clone https://github.com/dronekit/dronekit-python.git && \
  cd ./dronekit-python && \
  python setup.py build && \
  python setup.py install && \
  sed -i 's/, unsigned int,/, int,/' /usr/include/assert.h

COPY requirements.txt scripts/install-requirements.1.sh /sc/
RUN chmod +x /sc/install-requirements.1.sh && /sc/install-requirements.1.sh "/sc/requirements.txt"

WORKDIR /app
CMD [ "python3",  "src/main.py"]