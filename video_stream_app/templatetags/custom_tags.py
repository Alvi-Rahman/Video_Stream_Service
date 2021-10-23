from django import template
from django.utils import timezone

register = template.Library()


@register.filter(name='calculate_time')
def calculate_time(base_time, months):
    print(base_time)
    print(months)
    return f"{((base_time + timezone.timedelta(days=months*30)) - timezone.now()).days} Days"
