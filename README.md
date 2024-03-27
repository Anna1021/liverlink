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
The deployed version of the application can be found at [*liverlink.onrender.com*](https://liverlink.onrender.com).
The administrative interface can be found at [*liverlink.onrender.com/admin*](https://liverlink.onrender.com/admin).

Current admin access: @johndoe Password123

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

Throughout our project, we made use of Generative AI tools like ChatGPT and GitHub CoPilot. These tools played minor roles in testing, code refinement, and were used as a substitution for documentation to adhere to the project's dealine.

Code Optimization:
ChatGPT provided refactor suggestions for cleaner, more maintainable code.
GitHub CoPilot offered suggestions for code structure enhancement.
