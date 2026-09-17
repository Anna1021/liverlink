# Team Summertime Sadness Major Group project

## Team members
The members of the team are:
- YARA NIROUKH
- FABIHA CHOUDHURY
- RIYA GILL
- XINYAO (Anna) LIAO
- HANNAH PORTEOUS
- YIQING REN
- KATY WAKEMAN

## Project structure
The project is called `peer_support_network`.  It currently consists of a single app `peer_support`.

## Deployed version of the application
The deployed version of the application can be found at [*Liverly.pythonanywhere.com*](http://Liverly.pythonanywhere.com).
The administrative interface can be found at [*Liverly.pythonanywhere.com/admin*](http://Liverly.pythonanywhere.com/admin).

## Installation instructions
To install the software and use it in your local development environment, you must first set up and activate a local development environment.  From the root of the project:

```
$ virtualenv venv
$ source venv/bin/activate
```

Install all required packages:

```
$ pip3 install -r requirements.txt
```

Migrate the database:

```
$ python3 manage.py migrate
```

Seed the development database with:

```
$ python3 manage.py seed
```

Run all tests with:
```
$ python3 manage.py test
```

*The above instructions should work in your version of the application.  If there are deviations, declare those here in bold.  Otherwise, remove this line.*

## Render deployment

`render.yaml` defines a free Python web service and a separate PostgreSQL database.
Create a Blueprint from this repository in Render to provision both. Render allows
only one active free PostgreSQL database per workspace; the free database expires
after 30 days. If that slot is occupied, select a paid database or supply an
external `DATABASE_URL` when creating the web service manually.

- Build: `bash build.sh`
- Start: `python manage.py migrate --noinput && daphne -b 0.0.0.0 -p $PORT peer_support_network.asgi:application`
- Environment: `PYTHON_VERSION=3.11.11`, `DEBUG=False`, a generated `SECRET_KEY`,
  and `DATABASE_URL`.

The deployment creates database tables but does not copy the local SQLite data
or seed demo accounts. Run a single Daphne process: the current chat channel
layer is in memory and cannot be shared across multiple processes or instances.

## Sources
The packages used by this application are specified in `requirements.txt`

Initial scaffolding by Jeroen Keppens
https://emckclac-my.sharepoint.com/:w:/r/personal/k22007695_kcl_ac_uk/Documents/Sources.docx?d=w4b5451478d90421b82411597291b0083&csf=1&web=1&e=P43xZq
