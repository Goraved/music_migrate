#!/usr/bin/env bash
dir=$(pwd)


# Path to base folder of tests
PYTHONPATH="${PYTHONPATH}:${dir}"
export PYTHONPATH
# Setup virtual env
python3 -m pip install --user virtualenv  --quiet
python3 -m venv venv

source venv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt --quiet

python3 -m migrate_music.py