from django import template
from main.models import *
from django.db.models import Count

register = template.Library()

@register.filter
def mul(value, multiplier):
    return value * multiplier