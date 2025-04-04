#!/bin/sh
mkdir -p /var/log/gunicorn
chown -R appuser:appuser /var/log/gunicorn
exec "$@"