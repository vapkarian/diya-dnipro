#!/bin/bash

# Stop running on first error
set -e

# Default options
CELERY=true
BACKUPPATH=""
PULL=true
CLEAN=true
UPDATE=true
ENVIRONMENT="live"
MIGRATE=true
COLLECTSTATIC=true

# Parse arguments
while [[ $# > 0 ]]
do
    key="$1"
    case ${key} in
            -h|--help)
            echo "Update project and related packages"
            echo "Usage: ./deploy.sh [options]"
            echo "Options:"
            echo "  -no-celery           Do not turn off and turn on celery during deployment"
            echo "  --backuppath=PATH    Create backup of database and save it to the specified backup directory"
            echo "  -no-pull             Do not update source code from repository"
            echo "  -no-clean            Do not remove Python compiled files of project"
            echo "  -no-update           Do not update Python virtual environment"
            echo "  --env=ENVIRONMENT    Type of environment (either 'dev' or 'live', 'live' is default)"
            echo "  -no-migrate          Do not synchronize schema of database"
            echo "  -no-collectstatic    Do not collect static files (img, css, js)"
            echo "  -h, --help           Show this help message and exit"
            exit
        ;;
            -no-celery)
            CELERY=false
        ;;
            --backuppath=*)
            BACKUPPATH="${key#*=}"
        ;;
            -no-pull)
            PULL=false
        ;;
            -no-clean)
            CLEAN=false
        ;;
            -no-update)
            UPDATE=false
        ;;
            --env=*)
            ENVIRONMENT="${key#*=}"
            if [[ ! "dev live" =~ ${ENVIRONMENT} ]]; then
                echo "Unexpected env parameter! Exit."
                exit
            fi
        ;;
            -no-migrate)
            MIGRATE=false
        ;;
            -no-collectstatic)
            COLLECTSTATIC=false
        ;;
        *)
            echo "Unexpected parameter! Exit."
            exit
        ;;
    esac
shift
done

# Find root directory of project and set it as current directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.."
cd ${DIR}

# Stop celery worker if celery was installed
if [ "${CELERY}" = true ]; then
    if [ -r ${DIR}/env/bin/celery ]; then
        ${DIR}/env/bin/celery multi stopwait worker --pidfile=${DIR}/pids/%n.pid
    fi
fi

# Create backup of database (MySQL/PostgreSQL only)
if [ -n "${BACKUPPATH}" ]; then
    if [ -d ${BACKUPPATH} ]; then
        ${DIR}/commands/manage.sh dbdump --destination=${BACKUPPATH} --filename=$(date +%s).sql --compress=gzip
    fi
fi

# Update source code from repository
if [ "${PULL}" = true ]; then
    git pull
fi

# Remove Python compiled files
if [ "${CLEAN}" = true ]; then
    find ${DIR}/src -name '*.pyc' -delete
    find ${DIR}/src -name '__pycache__' -delete
fi

# Update existed and install new Python packages
if [ "${UPDATE}" = true ]; then
    rm -rf ${DIR}/env/src
    ${DIR}/env/bin/pip install --requirement=${DIR}/requirements/virtualenv/${ENVIRONMENT}.txt \
        --log=${DIR}/logs/build_pip_packages.log --log-file=${DIR}/logs/build_pip_packages_failures.log
fi

# Synchronize schema of database
if [ "${MIGRATE}" = true ]; then
    ${DIR}/env/bin/python ${DIR}/src/manage.py migrate
fi

# Collect static files (img, css, js)
if [ "${COLLECTSTATIC}" = true ]; then
    rm -r ${DIR}/static_content/static
    ${DIR}/env/bin/python ${DIR}/src/manage.py collectstatic --noinput
    ${DIR}/env/bin/python ${DIR}/src/manage.py compress
fi

# Update project by touching wsgi file
touch ${DIR}/src/wsgi.py

# Start celery worker if celery was installed
if [ "${CELERY}" = true ]; then
    if [ -r ${DIR}/env/bin/celery ]; then
        ${DIR}/env/bin/celery multi start -A psdnipro worker -B --events --workdir=${DIR}/src \
            --pidfile=${DIR}/pids/%n.pid --schedule=${DIR}/pids/celerybeat-schedule \
            --loglevel=info --logfile=${DIR}/logs/%n.log
    fi
fi

# Finish notification
echo "Successfully deployed!"
