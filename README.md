# pablo
> a mediocre fixture generator for django
## Installation
```
pip install django-pablo
```
## Setup
* Add `pablo` in `settings.py` of your django project
```
INSTALLED_APPS = (
    'django_prometheus',
    'rest_framework',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'pablo'
)
```
* just run `python manage.py pablo app_name.ModelName --limit 1 -v 1`
## Usage
```
usage: manage.py pablo [-h] [-l LIMIT] [-e EXCLUDE] [--debug] [--version] [-v {0,1,2,3}] [--settings SETTINGS] [--pythonpath PYTHONPATH] [--traceback] [--no-color]
                       [--force-color]
                       [app_label[.ModelName] ...]

Generate (sometimes)meaningful fixtures for your django project

positional arguments:
  app_label[.ModelName]
                        Restricts fixture to the specified app_label or app_label.ModelName

optional arguments:
  -h, --help            show this help message and exit
  -l LIMIT, --limit LIMIT
                        Limit number of fixtures generated for a model
  -e EXCLUDE, --exclude EXCLUDE
                        An app_label or app_label.ModelName to exclude (use multiple --exclude to exclude multiple apps/models)
  --debug               Enable verbosity with --debug flag
  --version             show program's version number and exit
  -v {0,1,2,3}, --verbosity {0,1,2,3}
                        Verbosity level; 0=minimal output, 1=normal output, 2=verbose output, 3=very verbose output
```

## Sample
<img width="720" src="https://i.imgur.com/BMw5sFQ.png"/>
