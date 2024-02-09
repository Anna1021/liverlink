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
The deployed version of the application can be found at [*enter url here*](*enter_url_here*).

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

## Sources
The packages used by this application are specified in `requirements.txt`

Initial scaffolding by Jeroen Keppens
https://emckclac-my.sharepoint.com/:w:/r/personal/k22007695_kcl_ac_uk/Documents/Sources.docx?d=w4b5451478d90421b82411597291b0083&csf=1&web=1&e=P43xZq
