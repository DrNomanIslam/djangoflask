from django import template
register = template.Library()

@register.filter()
def numeric(value):
    if type(value) == int or type(value) == float:
        return True
    else:
        return False
