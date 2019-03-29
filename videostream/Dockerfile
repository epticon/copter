FROM jrottenberg/ffmpeg:3.4-alpine

ARG APP_PATH=/usr/src/app
ARG ENTRY_FILE=entrypoint.sh

RUN mkdir -p ${APP_PATH}
COPY ${ENTRY_FILE} ${APP_PATH}

WORKDIR ${APP_PATH}
RUN chmod 744 ./${ENTRY_FILE}

ENTRYPOINT ./entrypoint.sh