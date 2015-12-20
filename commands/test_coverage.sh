#!/bin/bash

# Stop running on first error
set -e

# Find root directory of project and set it as current directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.."
cd ${DIR}

# Run coverage script for all project tests and save results
${DIR}/env/bin/coverage run --source='src/' ${DIR}/src/manage.py test --verbosity=0 --failfast ps
${DIR}/env/bin/coverage html
${DIR}/env/bin/coverage erase
echo Done, please visit /media/coverage/index.html
