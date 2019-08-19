from basketapp.models import Basket

def basketProc(request):
    print(f'context processor basket works')
    basket = []

    if request.user.is_authenticated:
        basket_items = Basket.objects.filter(user=request.user)
        for i in basket_items:
            basket.append(i.product.category.name)
            basket.append(i.product.name)
            basket.append(i.product.price)
    return {
        'BasketP': basket
    }
