#!/bin/sh

if ! [ -e venv ]
then
	virtualenv venv
	. venv/bin/activate
	pip3 install -r requirements.txt
	pip3 install -r ../server/requirements.txt
else
	. venv/bin/activate
fi

make html
