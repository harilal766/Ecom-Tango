#!/bin/bash

# Direcories
#PROJECT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
PROJECT_DIR=$(pwd)
VENV="venv"
VENV_PYTHON="$PROJECT_DIR/$VENV/bin/python3"

# Commands
cd $PROJECT_DIR

if [$VENV];
    python3 -m venv $VENV
    $VENV_PYTHON -m pip install -r requirements.txt
fi

$VENV_PYTHON "manage.py runserver 0.0.0.0:8000"