from django import template

register = template.Library()


@register.filter(name='access_by_key')
def access_by_key(value, arg):
    return value.get(arg)


@register.filter(name='access_by_index')
def access_by_index(value, arg):
    return value[arg]