#!/usr/bin/env sh

if [ ! -d "./env" ]; then
    virtualenv env
fi

source ./env/bin/activate
./env/bin/pip install -r requirements.txt
