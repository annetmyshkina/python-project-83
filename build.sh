#!/usr/bin/env bash
set -e

curl -fsSL https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

make install && psql -a -d $DATABASE_URL -f database.sql
