from django import template

register = template.Library()

@register.filter
def zip_lists(a, b):
    """Custom zip filter to zip two lists in templates."""
    return zip(a, b)
