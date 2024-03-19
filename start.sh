#!/bin/bash

# SPDX-FileCopyrightText: 2022 Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences
# SPDX-FileCopyrightText: 2024 Helmholtz Centre for Environmental Research (UFZ)
#
# SPDX-License-Identifier: CC0-1.0

set -e

cd "$(dirname "$0")"

#./wait-for.sh --timeout 300 "${POSTGREST_URL}"

poetry run python3 /opt/spotlight-migration/main.py "$@"
