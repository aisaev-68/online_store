from cart.cart import Cart


def cart(request):
    print(3333333, Cart(request))
    return {'cart': Cart(request)}