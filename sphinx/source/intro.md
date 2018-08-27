# How it works?

Appstore product from scratch for Ford using Flask web development skills
It provides user creation, application submission, database handling, giving
admin rights to other users, password recovery, and security to prevent
user's theft.

## Dependecies used (maybe this is unnecessary?)

* bcrypt==3.1.4
* blinker==1.4
* cffi==1.11.5
* click==6.7
* Flask==1.0.2
* Flask-Bcrypt==0.7.1
* flask-marshmallow==0.9.0
* flask-msearch==0.1.7
* Flask-SQLAlchemy==2.3.2
* Flask-WTF==0.14.2
* itsdangerous==0.24
* Jinja2==2.10
* MarkupSafe==1.0
* marshmallow==2.15.4
* marshmallow-sqlalchemy==0.14.1
* pycparser==2.18
* PyJWT==1.6.4
* six==1.11.0
* SQLAlchemy==1.2.10
* Werkzeug==0.14.1
* Whoosh==2.7.4
* WTForms==2.2.1
* flask-cors==3.0.6

## Python code snippet

```python
from setuptools import find_packages, setup

setup(
    name="vehicle_client",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "flask",
        "flask-sqlalchemy"
    ],
)
```

## Team

[Logan Kaser](https://github.com/logankaser)

[Zeid Tisnes](https://github.com/zedin27)

[Theo Walton](https://github.com/theo-walton)
