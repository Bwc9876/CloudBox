
from django import template
from django.forms import BoundField

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
