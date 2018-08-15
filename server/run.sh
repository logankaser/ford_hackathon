#!/bin/sh

if ! [ -e venv ]
then
virtualenv venv
pip3 install -r requirements.txt
fi
. venv/bin/activate

FLASK_APP="app_server" FLASK_DEBUG="TRUE" flask run