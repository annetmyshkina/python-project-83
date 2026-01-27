#!/usr/bin/env bash
set -e

curl -fsSL https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

make install

if [[ -n "${DATABASE_URL:-}" ]]; then
    psql -d "$DATABASE_URL" -f database.sql
else
  echo "DATABASE_URL не задан"
fi
