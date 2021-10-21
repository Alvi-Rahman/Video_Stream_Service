from django import template

register = template.Library()


@register.filter(name='calculate_total_price')
def calculate_total_price(price, unit):
    price = float(price)
    unit = int(unit)

    return price * unit
