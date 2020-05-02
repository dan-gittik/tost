#!/bin/bash

set -e
cd "$(dirname ${BASH_SOURCE[0]})/.."

rm -f db.sqlite3
./scripts/create-db.sh
