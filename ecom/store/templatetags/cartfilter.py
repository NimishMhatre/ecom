from django import template

register = template.Library()
@register.filter(name='is_in_cart')
def is_in_cart(product, cart):
    keys = cart.keys()

    for id in keys:
        if int(id) == product.id:
            return True
    return False


@register.filter(name='quantity_count')
def quantity_count(product, cart):
    keys = cart.keys()

    for id in keys:
        if int(id) == product.id:
            return cart.get(id)

    return 0


@register.filter(name='total_price')
def total_price(item, cart):
    return item.product.price * quantity_count(item.product, cart)