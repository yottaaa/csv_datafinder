from django import template
from django.utils.safestring import mark_safe 

register = template.Library()

@register.filter(name="mark")
def mark(content, search):
    result = content.replace(search, "<mark class='bg-warning'>{}</mark>".format(search))
    return mark_safe(result)