# SPDX-FileCopyrightText: 2022 Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences
# SPDX-FileCopyrightText: 2024 Helmholtz Centre for Environmental Research (UFZ)
#
# SPDX-License-Identifier: CC0-1.0

FROM python:3.12-slim

ENV POSTGREST_URL "http://localhost/api/v1"
ENV PGRST_JWT_SECRET "123"

WORKDIR /opt/spotlight-migration

COPY . .

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get upgrade -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y wget libmagick-dev && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install poetry && \
    poetry install

ENTRYPOINT [ "/opt/spotlight-migration/start.sh" ]
CMD ["--help"]
