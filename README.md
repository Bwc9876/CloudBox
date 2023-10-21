# Cloud Box

<p align="center">
<a href="https://github.com/Bwc9876/CloudBox"><img src="https://raw.githubusercontent.com/Bwc9876/CloudBox/main/.github/assets/Cloud_Box_Logo.png" alt="Cloud Box Logo"/></a><br/>
Cloud Box<br/>
</p>

A PaaS website for hosting remote VMs and SSH-ing into them. Built on top of Google Cloud Platform.

This is a site for Technica 2023, it was made using the following stack:

- Bootstrap
- Django
- Google Cloud
- Web SSH

## Building

### Prerequisites

- Python 3.11
- Poetry

### Development

```sh
poetry install
poetry run python manage.py migrate
poetry run python manage.py runserver
```

### Production

Still install dependencies and migrate:

```sh
poetry install
poetry run python manage.py migrate
```

In production, point the frontend web server to the WSGI module in `CloudBox/wsgi.py`

### Environment Variables

- `SECRET_KEY` - Secret key to use in Django
- `PROD` - `true` or `false`, whether we're in production
- `DOMAIN` - The domain to add to allowed hosts in Django

Environment variables are automatically loaded from a `.env` file in the root of the repo.
