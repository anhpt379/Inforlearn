"""django template tags for showing errors in UI
"""

__author__ = 'teemu@google.com (Teemu Kurppa)'

from django import template

register = template.Library()

@register.filter(name="error_to_html")
def error_to_html(error):
    return error.to_html()
