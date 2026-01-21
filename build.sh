#!/usr/bin/env bash

# Устанавливаем uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# Устанавливаем зависимости
make install

# Создаем таблицы в БД (работает как локально, так и на Render)
psql -d $DATABASE_URL -f database.sql
