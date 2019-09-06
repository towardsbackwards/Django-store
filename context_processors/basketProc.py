from django.shortcuts import render

from basketapp.models import Basket


def basketProc(request):
    print(f'context processor basket works')
    item1 = []
    item2 = []
    item3 = []
    item4 = []

    if request.user.is_authenticated:
        basket_items = Basket.objects.filter(user=request.user)
        if basket_items:                                                        #  basket_items = QuerySet
            for i in basket_items:
                item1.append(i.product.category.name)
                item2.append(i.product.name)
                item3.append(i.product.price)
                item4.append(i.quantity)
        basketzip = zip(item1, item2, item3, item4)
        print(len(Basket.objects.filter(user=request.user)))
        newbasket = (list(basketzip))
    return {'BasketP': newbasket}


'''def basketProc(request):
    basket = Basket.objects.filter(user=request.user).product.category.name
    return {'BasketP': basket}'''
