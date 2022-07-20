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

```bash
# install dependencies (only needs to be run once)
poetry install

# define database endpoint and JWT secret
export POSTGREST_URL=localhost:5432
export PGRST_JWT_SECRET=abcdef

# add spotlights to RSD database via PostgREST:
poetry run ./main.py
```
