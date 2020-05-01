#!/bin/bash

set -e
cd "$(dirname ${BASH_SOURCE[0]})/.."

python -m virtualenv .env --prompt='[tost] '
.env/bin/pip install -U pip
.env/bin/pip install -r requirements.txt
