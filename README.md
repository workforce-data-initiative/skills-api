# Open Skills API - Sharing the DNA of America's Jobs
Provides a complete and standard data store for canonical and emerging skills,
knowledge, abilities, tools, technolgies, and how they relate to jobs.

## Overview
TODO - Write a sweet, sweet overview of the API

## Demo
The following endpoints were automatically deployed via the Zappa framework to Amazon Web Services.
- [https://vhbg2y4qug.execute-api.us-east-1.amazonaws.com/dev/jobs](https://vhbg2y4qug.execute-api.us-east-1.amazonaws.com/dev/jobs)
- [https://vhbg2y4qug.execute-api.us-east-1.amazonaws.com/dev/skills](https://vhbg2y4qug.execute-api.us-east-1.amazonaws.com/dev/skills)

## Dependencies
- Python 2.7.11
- Postgres database

## Installation
To run the API locally, please perform the following steps:
1. Clone the repository from [https://www.github.com/dssg/skills-api](https://www.github.com/dssg/skills-api)
```
$ git clone https://www.github.com/dssg/skills-api
```
2. Navigate to the checked out project
```
$ cd skills-api
```
3. Ensure that pip package manager is installed. See installation instructions [here](https://pip.pypa.io/en/stable/installing/).
```
$ pip --version
```
4. Install the `virtualenv` package. Please review the [documentation](https://virtualenv.pypa.io/en/stable/) if you are unfamiliar with how `virtualenv` works.
```
$ pip install virtualenv
```
5. Create a Python 2.7.11 virtual environment called `venv` in the project root directory
```
$ virtualenv -p /path/to/python/2.7.11 venv
``` 
6. Activate the virtual environment. Note that the name of the virtual environment (`venv`) will be appended to the front of the command prompt. 
```
$ source venv/bin/activate 
(venv) $
```
7. Install dependencies from `requirements.txt`
```
$ pip install -r requirements.txt
```

8. Make regular (development) config. Run bin/make_config.sh and fill in connection string to database.
```
$ bin/make_config.sh
```

9. Clone development config for test config. Copy the resultant config/config.py to config/test_config.py and modify the SQL connection string to match your test database (you can leave this the same as your development database, if you wish, but we recommend keeping separate ones.
```
$ cp config/config.py config/test_config.py
```

## Deployment to Amazon Web Services
TODO - Write some deployment instructions here

## Dependencies
TODO - Write some dependencies.
