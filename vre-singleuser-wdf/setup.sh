#!/bin/bash
set -e
python /opt/setup-rucio-jupyterlab/configure.py
exec "$@"