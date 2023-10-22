from django import template
from django.conf import settings
from django.forms import BoundField
from django.utils.http import urlencode

register = template.Library()


@register.filter(name="obfuscate")
def obfuscate(value: str) -> str:
    char_codes = [str(ord(character)) for character in list(value)]
    return f'javascript:void(location.href="mailto:"+String.fromCharCode({",".join(char_codes)}))'


@register.filter(name="setup_field")
def setup_field(field: BoundField, with_placeholder=True) -> BoundField:
    validation_class = ""

    if field.errors:
        validation_class = "is-invalid"

    attrs = {
        "class": f"form-control {validation_class}",
        "aria-describedby": f"{field.name}-feedback",
    }

    if with_placeholder:
        attrs["placeholder"] = field.label

    new_field = field.as_widget(attrs=attrs)

    return new_field


@register.filter(name="get_ssh_link")
def get_ssh_link(box, request) -> str:
    hostname = request.get_host().split(":")[0]
    host = f"{request.scheme}://{hostname}:{settings.WEB_SSH_PORT}"
    params = {
        "title": f"SSH%20Connection%20To%20{box.name}",
        "hostname": box.ip,
        "port": 22,
        "username": "you",
        "privatekey": box.private_key,
    }
    return f"{host}/?{urlencode(params)}"
