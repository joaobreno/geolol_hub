#!/bin/sh
chown -R celery:celery /app
export > /app/.env
celery -A geolol_hub worker -E -l INFO --uid=celery