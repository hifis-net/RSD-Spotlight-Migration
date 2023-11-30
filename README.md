<!--
SPDX-FileCopyrightText: 2022 Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences
SPDX-FileCopyrightText: 2023 Helmholtz Centre for Environmental Research (UFZ)

SPDX-License-Identifier: CC-BY-4.0
-->

# Software Spotlight Migration for RSD

This repository provides a docker image to use in the RSD project to
migrate the spotlights from hifis.net or any other local source into
the RSD database structure.

## Run locally

If you have a RSD instance running locally you can start the migration with the
following commands:

### Install dependencies

```bash
# install dependencies (only needs to be run once)
poetry install
```

### Getting help

The tool supports some command line arguments:

```shell
$ poetry run ./main.py -h
usage: main.py [OPTION] PATH

Migrate Software spotlights from a local file path to the RSD.

positional arguments:
  PATH                  The file path where to find the spotlights.

options:
  -h, --help            show this help message and exit
  -d, --delete_all      Delete all spotlights and overwrite with current versions.
  -i, --update_imprint  Update imprint if it already exists.
  -v, --verbose         Increase verbosity.
```

### Run migration

Define the required environment variables as specified in your RSD `frontend/.env.local`

```bash
# define POSTGREST API endpoint and JWT secret
export POSTGREST_URL=https://localhost/api/v1
export PGRST_JWT_SECRET=abcdef

# add spotlights to RSD database via PostgREST:
poetry run ./main.py
```

or import them directly from your `.env.local`:

```bash
set -a
source ~/path/to/RSD-as-a-service/frontend/.env.local
poetry run ./main.py
```
