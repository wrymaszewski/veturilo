from django import template

register = template.Library()

@register.filter
def get_lat(value):
    return float(value.split(',')[0])

@register.filter
def get_lng(value):
    return float(value.split(',')[1])
