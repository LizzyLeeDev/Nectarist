from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dict, key):
    return dict[key]

@register.simple_tag
def define(val=None):
  return val