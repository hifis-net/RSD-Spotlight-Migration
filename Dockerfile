# SPDX-FileCopyrightText: 2022 Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences
#
# SPDX-License-Identifier: CC0-1.0

FROM python:3.9-bullseye

ENV POSTGREST_URL "http://localhost/api/v1"
ENV PGRST_JWT_SECRET "123"

WORKDIR /opt/spotlight-migration

COPY . .

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get upgrade -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y wget && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install poetry && \
    poetry install

CMD [ "/opt/spotlight-migration/start.sh" ]
