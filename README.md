RESTaurant
===

Django Rest framework + Azure App Service + MySQL + CI/CD by GitHub Actions = test

![readme](https://user-images.githubusercontent.com/28250432/104155388-73050300-542a-11eb-9e16-a9d3fae927d8.png)

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
