# shard-research [![](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/) [![](https://img.shields.io/badge/django-4.2-green.svg)](https://www.python.org/downloads/) [![](https://img.shields.io/badge/drf-3.14-red.svg)](https://www.python.org/downloads/)  


## Backend Directory Structure
```
└── backend
    ├── app              # django app directory
    ├── config           # django config directory
    └── templates        # django template directory
```


## Package
- [requirements.txt](./backend/requirements.txt)


## Create Dummy Data
```
python manage.py dummy [app_name.model_name] -n 10
```


## Run Server
```
python manage.py runserver 0:8000
```


## API Document
- http://api.localhost:8000/swagger/

