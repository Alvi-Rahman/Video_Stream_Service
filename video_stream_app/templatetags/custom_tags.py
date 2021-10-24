from django import template
from django.utils import timezone

register = template.Library()


@register.filter(name='calculate_time')
def calculate_time(base_time, months, views=False):
    try:
        if views:
            return ((base_time + timezone.timedelta(days=months*30)) - timezone.now()).days
        else:
            return f"{((base_time + timezone.timedelta(days=months*30)) - timezone.now()).days} Days"
    except:
        return None
