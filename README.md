RESTaurant
===

Django Rest framework + Azure App Service + MySQL + CI/CD by GitHub Actions = test

## Installation

```bash
pipenv install
pipenv shell
python manage.py migrate
python manage.py createsuperuser --email admin@example.com --username admin
python manage.py runserver
```

## What are included

- [Official tutorials](https://www.django-rest-framework.org/tutorial/quickstart/)
- Continuous deployment and schedule api call using GitHub Actions
- Custom command
