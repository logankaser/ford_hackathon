#!/bin/sh

NAME=example_app
virtualenv -p $(which python3.7) .build_env
source .build_env/bin/activate
pip install pex wheel
mkdir -p build
pip wheel -w build .
mkdir -p dist
pex . -r requirements.txt --disable-cache -f build $NAME -e $NAME.main -o dist/$NAME
deactivate
rm -rf .build_env build
