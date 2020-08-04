#!/bin/bash -e

gunicorn --workers=4 \
  --bind=0.0.0.0:8000 \
  --worker-tmp-dir=/dev/shm \
  -e SCRIPT_NAME=$APPLICATION_ROOT \
  --log-file=/log/gunicorn.log \
  --access-logfile=/log/gunicorn-access.log \
  "pyscriptdeck:create_app()"
