#!/bin/bash

# Stop running on first error
set -e

# Find root directory of project
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.."

# Start celery monitoring if celery was installed
if [ -r ${DIR}/env/bin/celery ]; then
    ${DIR}/env/bin/celery -A ps events --workdir=${DIR}/src
fi
