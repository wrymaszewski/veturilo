from django import template

register = template.Library()


@register.filter
def get_coord(value, coord='lat'):
    lat, lng = value.split(',')
    if coord == 'lng':
        return float(lng)
    else:
        return float(lat)
