FROM python:3.8-alpine as builder

RUN apk add --no-cache bash mariadb-dev jpeg-dev zlib-dev libjpeg
RUN apk add --no-cache cmake make git openssh gcc g++ musl-dev linux-headers mysql-client libffi-dev rust cargo flex bison

ARG CI_REGISTRY_USER
ARG CI_JOB_TOKEN
ARG CI_PROJECT_ID
ARG CI_REPOSITORY_PYPI_URL

ENV VENV=/venv
ENV PATH="$VENV/bin:$PATH"

RUN python -m venv $VENV

#RUN pip config --site set global.trusted-host $CS_HOST_BASE
#RUN pip config --site set global.extra-index-url http://${CS_USER}:${CS_PW}@${CS_DISTRIB_URL}
#RUN pip config --site set global.trusted-host $CI_API_V4_URL
RUN pip config --site set global.extra-index-url https://${CI_REGISTRY_USER}:${CI_JOB_TOKEN}@${CI_REPOSITORY_PYPI_URL}/simple
RUN pip config --site set global.no-cache-dir false

# install guncorn for serving the wsgi scripts
RUN pip install --no-cache-dir wheel gunicorn
RUN pip install --no-cache-dir webob

# install the WFM
WORKDIR /checkouts
COPY . .
RUN pip --no-cache-dir install .

FROM python:3.8-alpine

RUN apk add --update --no-cache bash mariadb-dev
# RUN apk add --no-cache jpeg-dev zlib-dev libjpeg

# force using bash shell
SHELL ["/bin/bash", "-c"]

ENV VENV=/venv
ENV PATH="$VENV/bin:$PATH"

ENV SITE_CONFIG='. ${TOP_WWPDB_SITE_CONFIG_DIR}/init/env.sh --siteid ${WWPDB_SITE_ID} --location ${WWPDB_SITE_LOC}'
ENV WRITE_SITE_CONFIG_CACHE='ConfigInfoFileExec --siteid $WWPDB_SITE_ID --locid $WWPDB_SITE_LOC --writecache'

COPY --from=builder $VENV $VENV

ENV RUN_SCRIPT=/run_app.sh
RUN echo "${SITE_CONFIG}" >> ${RUN_SCRIPT} \
    && echo "gunicorn wwpdb.apps.editormodule.webapp.wsgi --bind 0.0.0.0:8080 --timeout 0 --threads 4" >> ${RUN_SCRIPT} \
    && chmod a+x ${RUN_SCRIPT}

CMD ${RUN_SCRIPT}
