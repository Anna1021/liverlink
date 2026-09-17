# Peer Support — LiverLink

A Django peer support application with profiles, posts, questions, peer matching,
notifications, moderation, and live conversations using Django Channels.

- Repository: [Anna1021/liverlink](https://github.com/Anna1021/liverlink)
- Website: [peer-support-vpxu.onrender.com](https://peer-support-vpxu.onrender.com)

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
The deployed version of the application can be found at [*peer-support-vpxu.onrender.com*](https://peer-support-vpxu.onrender.com).
The administrative interface can be found at [*peer-support-vpxu.onrender.com/admin*](https://peer-support-vpxu.onrender.com/admin).

Production accounts are created separately; development seed accounts are not deployed.

## Installation instructions
Use Python 3.11 (Render currently uses 3.11.11). From the project root:

```
$ python3.11 -m venv venv
$ source venv/bin/activate
$ export DEBUG=True
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

Seeding is optional and intended for local development only. To run the app:

```sh
python manage.py runserver
```

Local development uses SQLite unless `DATABASE_URL` is set. To create your own
administrator account, run `python manage.py createsuperuser`.

Run all tests with:
```
$ python3 manage.py test
```

The full suite includes Selenium tests that require Chrome and a compatible
ChromeDriver. To run the backend suite without browser dependencies:

```sh
python manage.py test peer_support.tests.models peer_support.tests.forms peer_support.tests.views peer_support.tests.templatetags
```

## Render deployment

`render.yaml` defines a free Python web service and a separate PostgreSQL database.
The existing service tracks this repository's `main` branch and deploys on push.
Create a Blueprint from this repository in Render to provision both. Render allows
only one active free PostgreSQL database per workspace; the free database expires
after 30 days. If that slot is occupied, select a paid database or supply an
external `DATABASE_URL` when creating the web service manually.

- Build: `bash build.sh`
- Start: `python manage.py migrate --noinput && python manage.py seed_once && daphne -b 0.0.0.0 -p $PORT peer_support_network.asgi:application`
- Environment: `PYTHON_VERSION=3.11.11`, `DEBUG=False`, a generated `SECRET_KEY`,
  and `DATABASE_URL`.

The deployment creates database tables but does not copy the local SQLite data.
Demo data is loaded with the idempotent `python manage.py seed_once` command. The seeded test
administrator is `@johndoe` with password `Password123`. Run a single Daphne
process: the current chat channel layer is in memory and cannot be shared across
multiple processes or instances.

### Upgrading an existing database

Run `python manage.py migrate` (the Render start command already does this).
The original `0001_initial` migration is preserved for existing installations.
Migration `0002` applies upstream model changes, and `0003` updates saved avatar
paths to the renamed image files while preserving users and their avatar choices.
Do not replace the database or add the non-idempotent `seed` command to the
permanent start command.

## Sources
The packages used by this application are specified in `requirements.txt`

Initial scaffolding by Jeroen Keppens

Throughout our project, we made use of Generative AI tools like ChatGPT and GitHub CoPilot. These tools played minor roles in testing, code refinement, and were used as a substitution for documentation to adhere to the project's dealine.

Code Optimization:
ChatGPT provided refactor suggestions for cleaner, more maintainable code.
GitHub CoPilot offered suggestions for code structure enhancement.
