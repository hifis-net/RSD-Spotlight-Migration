#!/bin/bash

set -e

cd "$(dirname "$0")"

./wait-for.sh --timeout 300 "${POSTGREST_URL}"

poetry run python3 /opt/spotlight-migration/main.py
