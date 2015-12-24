#!/bin/bash

# Stop running on first error
set -e

# Default options
PACKAGE_MANAGER_COMMAND="sudo apt-get install"
ENVIRONMENT="live"
PYTHON_EXECUTABLE="python3.5"

# Parse arguments
while [[ $# > 0 ]]
do
    key="$1"
    case ${key} in
            -h|--help)
            echo "Install initial environment of project"
            echo "Usage: ./initial.sh [options]"
            echo "Options:"
            echo "  --manager=MANAGER    OS-specific run command for dependencies ('sudo apt-get install' is default)"
            echo "  --env=ENVIRONMENT    Type of environment (either 'dev' or 'live', 'live' is default)"
            echo "  --python=PYTHON      Specify the Python executable ('python3.5' is default)"
            echo "  -h, --help           Show this help message and exit"
            exit
        ;;
            --manager=*)
            PACKAGE_MANAGER_COMMAND="${key#*=}"
        ;;
            --env=*)
            ENVIRONMENT="${key#*=}"
            if [[ ! "dev live" =~ ${ENVIRONMENT} ]]; then
                echo "Unexpected env parameter! Exit."
                exit
            fi
        ;;
            --python=*)
            PYTHON_EXECUTABLE="${key#*=}"
        ;;
        *)
            echo "Unexpected parameter! Exit."
            exit
        ;;
    esac
shift
done

# Find root directory of project
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.."
cd ${DIR}

# Install dependencies
${PACKAGE_MANAGER_COMMAND} $(cat ${DIR}/requirements/os/common.txt)
if [ -r ${DIR}/requirements/os/${ENVIRONMENT}.txt ]; then
    ${PACKAGE_MANAGER_COMMAND} $(cat ${DIR}/requirements/os/${ENVIRONMENT}.txt)
fi

# Create necessary project directories
mkdir ${DIR}/configs
mkdir ${DIR}/logs
mkdir ${DIR}/pids
mkdir ${DIR}/static_content
mkdir ${DIR}/static_content/media

# Create virtual environment for Python packages
virtualenv -p ${PYTHON_EXECUTABLE} --prompt="<env>" ${DIR}/env
