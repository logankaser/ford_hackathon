#!/bin/sh

NAME=gui
virtualenv -p $(which python3) .build_env
source .build_env/bin/activate
pip install pex wheel
mkdir -p build
pip wheel -w build .
pex . -r requirements.txt --disable-cache -f build $NAME -e $NAME.main -o package/app/$NAME
deactivate
cd package
tar cf $NAME.tar app app.json
gzip $NAME.tar
cd ..
mv package/$NAME.tar.gz .
rm -rf .build_env build $NAME.egg-info
