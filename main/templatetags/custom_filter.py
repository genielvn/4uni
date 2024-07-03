from django import template
from django.utils.timesince import timesince

register = template.Library()

@register.filter
def timesince_short(value):
    result = timesince(value)
    return result.split(', ')[0]
