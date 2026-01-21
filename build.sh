#!/usr/bin/env bash
set -e

curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

make install

# 🔥 ОТЛАДКА: покажем ВСЕ переменные
echo "🔍 DEBUG: Все переменные окружения:"
env | grep -i database || echo "❌ DATABASE_URL ОТСУТСТВУЕТ!"
echo "🔍 DATABASE_URL = '$DATABASE_URL'"
echo "🔍 Длина DATABASE_URL = ${#DATABASE_URL} символов"

if [ -n "$DATABASE_URL" ] && [ "$DATABASE_URL" != "" ]; then
    echo "🎯 Миграция БД: $DATABASE_URL"
    psql "$DATABASE_URL" -c "SELECT 1" && echo "✅ Тест подключения OK"
    psql "$DATABASE_URL" -f database.sql
    echo "✅ Таблицы созданы"
else
    echo "❌ ОШИБКА: DATABASE_URL пустая или отсутствует!"
    echo "   Проверьте Render Dashboard → Environment"
    exit 1
fi

