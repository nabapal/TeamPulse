from django import template
from django.urls import reverse, NoReverseMatch

register = template.Library()

@register.simple_tag(takes_context=True)
def is_active(context, view_name):
    request = context['request']
    try:
        if request.resolver_match.view_name == view_name:
            return 'active'
        if 'reports' in view_name and 'reports' in request.resolver_match.view_name:
            return 'active'
    except AttributeError:
        pass
    return ''
