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
    pip3 install poetry && \
    poetry install && \
    wget "https://raw.githubusercontent.com/eficode/wait-for/v2.2.3/wait-for" -O wait-for.sh && \
    chmod +x wait-for.sh

CMD [ "/opt/spotlight-migration/start.sh" ]
