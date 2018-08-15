#!/bin/sh

if ! [ -e venv ]
then
	virtualenv venv
	. venv/bin/activate
	pip3 install -r requirements.txt
else
	. venv/bin/activate
fi

FLASK_APP="app_server" FLASK_DEBUG="TRUE" flask run
