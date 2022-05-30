from django.template.defaulttags import register

@register.filter
def get_all_from_cart_products(cart_products):
    return [cart_product.boardgame for cart_product in cart_products] if cart_products else []