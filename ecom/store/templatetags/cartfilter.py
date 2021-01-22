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

@register.filter(name='total_cart_price')
def total_cart_price(products, cart):
    sum = 0
    for p in products:
        sum += total_price(p, cart)

    return sum


@register.filter(name='currency')
def currency(number):
    return "₹ "+str(number)



@register.filter(name='multiply')
def multiply(number , number1):
    return number * number1