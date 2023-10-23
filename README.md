# Cloud Box

<p align="center">
<a href="https://github.com/Bwc9876/CloudBox"><img src="https://raw.githubusercontent.com/Bwc9876/CloudBox/main/.github/assets/Cloud_Box_Logo.png" alt="Cloud Box Logo"/></a><br/>
<strong>Cloud Box</strong><br/>
</p>

<br/>

A website for hosting remote VMs and SSH-ing into them. Built on top of the Google Cloud Platform.

This is a site for [Technica 2023](https://technica-2023.devpost.com/), it was made using the following stack:

- Bootstrap
- Django
- Google Cloud
- Web SSH

## Screenshots

![The Main Page](https://github.com/Bwc9876/CloudBox/assets/25644444/7f6a83cd-4bfb-45b6-a7fe-a2b7e2351045)  
*The main page*

![List of Boxes the User Has](https://github.com/Bwc9876/CloudBox/assets/25644444/5d5e2d67-e9fb-4f27-bea5-d877e6ea26ed)  
*The Box list page where the user can create and run boxes*

![SSH acces to a box](https://github.com/Bwc9876/CloudBox/assets/25644444/5587fc0a-3d01-4b08-b17b-c56b6958eed1)  
*SSH Access to a box running `cowsay`*

## Building

### Prerequisites

- Python 3.11
- Poetry
- Web SSH

> ⚠️ **Warning**:  
> Web SSH needs to be running and listening on port 8001 for SSH access to work

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

In production, point the frontend web server to the WSGI module in `cloud_box.wsgi`

```sh
poetry run gunicorn cloud_box.wsgi
```

### Environment Variables

- `SECRET_KEY` - Secret key to use in Django
- `PROD` - `true` or `false`, whether we're in production
- `DOMAIN` - The domain to add to allowed hosts in Django
