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

Throughout our project, we made effective use of advanced Generative AI tools like ChatGPT and GitHub CoPilot. These tools played a key role in testing, code refinement, and quick issue resolution.

Testing Efficiency:
ChatGPT generated test cases, ensuring comprehensive test coverage.
GitHub CoPilot suggested test snippets.

Code Optimization:
ChatGPT provided refactor suggestions for cleaner, more maintainable code.
GitHub CoPilot offered intelligent recommendations for code structure enhancement.

Swift Issue Resolution:
ChatGPT generated potential solutions and debug steps, aiding in faster problem resolution.
GitHub CoPilot suggested fixes for minor bugs and code inconsistencies.

Documentation Support:
Both tools improved project documentation with clearer explanations and usage examples.
