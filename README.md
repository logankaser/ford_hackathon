# Ford hackathon

[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)

# About

Car Appstore from scratch for the Ford hackathon using Flask.

<img src="resources/login.png" width="40%"><img src="resources/app_overview.png" width="40%">
<img src="resources/admin_panel.png" width="50%">

### Features
* User creation
* User roles
* Application submission and approval
* Application checksum verification
* Multiple Application Types
* Password recovery
* SPA Client

### Major Dependecies
* [Flask (HTTPS Handlers)](http://flask.pocoo.org/docs/1.0/)
* [Flask-Bcrypt (Password hashing and salting)](https://flask-bcrypt.readthedocs.io/en/latest/)
* [Flask-SQLAlchemy (SQL ORM)](http://flask-sqlalchemy.pocoo.org/2.3/)
* [Flask-Marshmallow (JSON Serialization)](https://flask-marshmallow.readthedocs.io/en/latest/)
* [Hyperapp (Javascript SPA client)](https://hyperapp.js.org/)


## Client

### Running
`cd client` and start with `./run.sh`
view at `localhost:5000`

## Server

### Running

`cd server` and start with `./run.sh`
view at `localhost:5000/login`

## [Docs (click me)](https://doc.fordhackathon.com/)

### Generating
`cd sphinx` and `./docs.sh`

### Team

[Logan Kaser](https://github.com/logankaser)

[Zeid Tisnes](https://github.com/zedin27)

[Theo Walton](https://github.com/theo-walton)
