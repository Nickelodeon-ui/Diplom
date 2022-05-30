import imp
from django.template.defaulttags import register

@register.filter
def startswith(text, starts):
    return text.startswith(starts)
    