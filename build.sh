#!/usr/bin/env bash
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
make install

if [ -n "$DATABASE_URL" ]; then
    psql "$DATABASE_URL" -f database.sql -v ON_ERROR_STOP=1
else
    exit 0
fi

