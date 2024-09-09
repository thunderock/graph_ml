#!/bin/bash

echo "Init vscode integrated terminal"

ENV_FILE=".env"
VENV_DIR=".venv/bin/activate"

if test -f ~/.bash_profile; then
    echo "Running ~/.bash_profile"
    source ~/.bash_profile
fi

if test -f "$ENV_FILE"; then
    echo "Exporting env vars in $ENV_FILE"
    set -o allexport
    source "$ENV_FILE"
    set +o allexport
fi

if test -f "$VENV_DIR"; then
    echo "Activating virtualenv"
    source "$VENV_DIR"
fi
