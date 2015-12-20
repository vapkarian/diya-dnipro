Required system package requirements:
    python3.5 python3.5-dev python3-setuptools virtualenv gcc libjpeg8-dev

Optional system package requirements (database, cache):
    memcached rabbitmq-server libpq-dev postgresql postgresql-contrib

Server-side system package requirements (web-server):
    nginx supervisor

There are several bash scripts in "commands" directory:
    1. initial.sh - script for create dir structure and python virtual environment (so all projects libs like django and other third-party libs will be installed only for this project and isolated for system). You should run this command once after "git checkout";
    2. deploy.sh - script for updating project and python virtual environment. You should run this command for each update;
    3. manage.sh - script for calling any manage.py commands;
    4. monitor.sh - script for starting event-stream utilities for monitoring celery tasks in real time;
    5. test_coverage.sh - script for running unit-tests of project and creating coverage report (you can see it at /media/coverage/index.html).
