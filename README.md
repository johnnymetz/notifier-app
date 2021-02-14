# Notifier App

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/psf/black)
[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=for-the-badge)](https://github.com/prettier/prettier)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&style=for-the-badge)](https://github.com/pre-commit/pre-commit)

![Django](https://img.shields.io/badge/-Django-092E20?logo=Django&style=for-the-badge)
![PostgreSQL](https://img.shields.io/badge/postgres-%23316192.svg?logo=postgresql&style=for-the-badge)
![React](https://img.shields.io/badge/react%20-%2320232a.svg?logo=react&style=for-the-badge)
![Bootstrap](https://img.shields.io/badge/-Bootstrap-563D7C?logo=bootstrap&style=for-the-badge)
![Heroku](https://img.shields.io/badge/heroku%20-%23430098.svg?logo=heroku&style=for-the-badge)
![Docker](https://img.shields.io/badge/docker%20-%230db7ed.svg?logo=docker&logoColor=white&style=for-the-badge)

Send yourself daily email notifications.

## Todo

- Dockerize cypress tests
- Upgrade djoser so activation email isn't sent on user update (e.g. subscribe on/off)
- Use direct type hints (once mypy supports it)
- Address TODOs in code
- Try an XSS attack: [XSS Exploitation in Django Applications](https://tonybaloney.github.io/posts/xss-exploitation-in-django.html)

## Todo (maybe later)

- Move config files to pyproject.toml
- Papertrail heroku plugin
- Sendgrid batch api
- Unit test emails
- Freezegun should be able to choose a timezone
  so I don't need to set settings.TIME_ZONE = "UTC" in the first line of every test.
  If no luck, try [time-machine](https://github.com/adamchainz/time-machine)
- PR in django-extensions to raise error on `create_command` if file already exists
- Scan site with [Mozilla Observatory](https://observatory.mozilla.org/)
- [Add security.txt to .well-known endpoint](https://adamj.eu/tech/2020/06/28/how-to-add-a-well-known-url-to-your-django-site/)
- [Maybe add robots endpoint](https://adamj.eu/tech/2020/02/10/robots-txt/)
- Create splash page
- Add holidays

## Resources

- [Production deployment checklist](https://testdriven.io/blog/production-django-deployments-on-heroku/)
- [SendGrid web api vs. SMTP](https://sendgrid.com/blog/web-api-or-smtp-relay-how-should-you-send-your-mail/)
  - Web api:
    - [django-sendgrid-v5](https://github.com/sklarsa/django-sendgrid-v5)
    - (OR) [sendgrid-django](https://github.com/elbuo8/sendgrid-django)
  - SMPT: [no extra package necessary](https://sendgrid.com/docs/for-developers/sending-email/django/)
- [Using Postgres Row-Level Security in Python and Django](https://pganalyze.com/blog/postgres-row-level-security-django-python)
- [Installing system packages in Docker with minimal bloat](https://pythonspeed.com/articles/system-packages-docker/)
- [super-linter](https://github.com/github/super-linter)
- [flake8-awesome](https://github.com/afonasev/flake8-awesome)
- [django-migration-linter](https://github.com/3YOURMIND/django-migration-linter)
