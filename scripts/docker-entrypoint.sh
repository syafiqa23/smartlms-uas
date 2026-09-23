#!/bin/sh
set -e

if [ -n "${POSTGRES_HOST:-}" ]; then
  echo "Waiting for PostgreSQL at $POSTGRES_HOST:${POSTGRES_PORT:-5432}..."
  until nc -z "$POSTGRES_HOST" "${POSTGRES_PORT:-5432}"; do
    sleep 1
  done
fi

if [ "${RUN_MIGRATIONS:-False}" = "True" ]; then
  python manage.py migrate --noinput
fi

if [ "${RUN_COLLECTSTATIC:-True}" = "True" ]; then
  python manage.py collectstatic --noinput
fi

exec "$@"
