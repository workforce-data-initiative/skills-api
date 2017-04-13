# Open Skills API - Sharing the DNA of America's Jobs
Provides a complete and standard data store for canonical and emerging skills,
knowledge, abilities, tools, technolgies, and how they relate to jobs.

## Overview
A web application to serve the [Open Skills API](http://api.dataatwork.org/v1/spec/).

An overview of the API is maintained in this repository's Wiki: [API Overview](https://github.com/workforce-data-initiative/skills-api/wiki/API-Overview)


## Loading Data
The data necessary to drive the Open Skills API is loaded through the tasks present in the [skills-airflow](https://github.com/workforce-data-initiative/skills-airflow/) project. Follow the instructions in that repo to run the workflow and load data into a database, along with an Elasticsearch endpoint. You will use the database credentials and Elasticsearch endpoint when configuring this application.

## Dependencies
- Python 2.7.11
- Postgres database with skills and jobs data loaded. (see skills-airflow note above)
- Elasticsearch 5.x instance with job normalization data loaded (see skills-airflow note above)

## Installation
To run the API locally, please perform the following steps:
1. Clone the repository from [https://www.github.com/workforce-data-initiative/skills-api](https://www.github.com/workforce-data-initiative/skills-api)
```
$ git clone https://www.github.com/workforce-data-initiative/skills-api
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

8. Make regular (development) config. Run bin/make_config.sh and fill in connection string to the database used in skills-airflow.
```
$ bin/make_config.sh
```

9. Add an ELASTICSEARCH_HOST variable to config/config.py to point to the Elasticsearch instance that holds the job normalization data from skills-airflow

10. Clone development config for test config. Copy the resultant config/config.py to config/test_config.py and modify the SQL connection string to match your test database (you can leave this the same as your development database, if you wish, but we recommend keeping separate ones.
```
$ cp config/config.py config/test_config.py
```

Now you can run the Flask server.
```
(venv) $ python server.py runserver
```

Navigate to `http://127.0.0.1:5000/v1/jobs` and you should see a listing of jobs. You can check out more endpoints at the [API Specification](http://127.0.0.1:5000/v1/jobs)
