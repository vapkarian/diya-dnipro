#!/bin/bash

# Stop running on first error
set -e

# Find root directory of project
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.."

# Run django manage script with provided parameters
${DIR}/env/bin/python ${DIR}/src/manage.py $*
