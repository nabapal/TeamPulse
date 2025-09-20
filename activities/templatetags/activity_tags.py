from django import template

register = template.Library()

@register.filter
def status_color(status_name):
    if status_name == 'Completed':
        return 'success'
    elif status_name == 'In Progress':
        return 'warning'
    elif status_name == 'On Hold':
        return 'danger'
    elif status_name == 'Yet to Start':
        return 'primary'
    else:
        return 'secondary'
