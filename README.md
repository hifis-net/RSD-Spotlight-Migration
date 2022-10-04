<!--
SPDX-FileCopyrightText: 2022 Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences

SPDX-License-Identifier: CC-BY-4.0
-->

# hifis.net Spotlight Migration for RSD

This repository provides a docker image to use in the RSD project to
migrate the spotlights from hifis.net into the RSD database structure.

We use Git submodules, so be sure to clone recursively or initialize the
submodules after cloning:

```bash
git clone --recurse-submodules ...
# or:
git clone ...
git submodule init
git submodule update
```

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
$ poetry run ./main.py --help
usage: main.py [OPTION]

Migrate Software spotlights from hifis.net to the RSD.

options:
  -h, --help            show this help message and exit
  -d, --delete_all      Delete all spotlights and overwrite with current versions.
  -i, --update_imprint  Update imprint if it already exists.
  -v, --verbose         Increase verbosity.
```

### Run migration

Define the required environment variables as specified in your RSD `frontend/.env.local`

```bash
# define database endpoint and JWT secret
export POSTGREST_URL=localhost:5432
export PGRST_JWT_SECRET=abcdef

# add spotlights to RSD database via PostgREST:
poetry run ./main.py
```

or import them directly from you `.env.local`:

```bash
set -a
source ~/path/to/RSD-as-a-service/frontend/.env.local
poetry run ./main.py
```
