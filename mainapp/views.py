from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import datetime
import json, os
from mainapp.models import Product, TrendyProduct, ContactCard, TopSliderProduct, Category, HotSliderProduct
from basketapp.models import Basket
from django.contrib.auth.decorators import login_required, user_passes_test
import random
from django.views.generic import ListView

# Create your views here.
current_date_text = 'Current date and time is: '
current_date_text = current_date_text.upper()
current_datetime = datetime.datetime.now()

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static',
                                    'data.json'))  # вышли из mainapp и зашли в статику к файлу data.json
with open(path) as json_data:
    data = json.load(json_data)
    json_data.close()


def main_view(request):
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    slider_product = TopSliderProduct.objects.all()
    hot_product = HotSliderProduct.objects.all()
    trendy_products = TrendyProduct.objects.all()[:6]  # максимум 6 первых (чтобы не перегружать страницу)
    content = {
        'datetime': current_datetime,
        'date_text': current_date_text,
        'data': data,
        'trendy': trendy_products,
        'slider_product': slider_product,
        'hot_product': hot_product,
        'basket': basket,
    }
    return render(request, 'index.html', content)


def contact_view(request):
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    contact_cards = ContactCard.objects.all()
    return render(request, 'contact.html',
                  {'contact_card': contact_cards, 'datetime': current_datetime, 'date_text': current_date_text,
                   'data': data, 'basket': basket})


def get_hot_product():
    products = Product.objects.all()

    return random.sample(list(products), 1)[0]  # возвращает 1 случайный продукт из всех


def products_view(request, pk=None, page=1):
    trendy_products = TrendyProduct.objects.all()
    title = 'продукты'
    links_menu = Category.objects.all()
    basket = []
    hot_product = get_hot_product()  # ТОТ самый рандомайзер
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    if pk:
        if pk == '0':
            products = Product.objects.all().order_by('price')
            category = {'name': 'All'}
        else:
            category = get_object_or_404(Category, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')

        paginator = Paginator(products, 2)
        try:
            # получение объектов нужной сраницы
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            # последняя страница
            products_paginator = paginator.page(paginator.num_pages)

        print(type(products))
        print(type(products_paginator))
        print(len(list(products)))
        content = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': products,
            'datetime': current_datetime,
            'date_text': current_date_text,
            'data': data,  # JSON
            'new_products': trendy_products,
            'basket': basket,
            'hot_product': hot_product,
        }
        return render(request, 'products.html', content)
    content = {
        'title': title,
        'links_menu': links_menu,
        'datetime': current_datetime,
        'date_text': current_date_text,
        'data': data,  # JSON
        'new_products': trendy_products,
        'basket': basket,
        'hot_product': hot_product,
    }
    return render(request, 'products.html', content)