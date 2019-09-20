from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import datetime
import json, os
from mainapp.models import Product, TrendyProduct, ContactCard, Category
from basketapp.models import Basket
from django.contrib.auth.decorators import login_required, user_passes_test
import random
from django.views.generic import ListView
from django.conf import settings
from django.core.cache import cache
from django.views.decorators.cache import cache_page

# Create your views here.
current_date_text = 'Current date and time is: '
current_date_text = current_date_text.upper()
current_datetime = datetime.datetime.now()

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static',
                                    'data.json'))  # вышли из mainapp и зашли в статику к файлу data.json
with open(path) as json_data:
    data = json.load(json_data)
    json_data.close()

    # ===============================LOW CACHE=================================


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            # print(f'caching {key}')
            links_menu = Category.objects.all
            cache.set(key, links_menu)
        return links_menu
    else:
        return Category.objects.all


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(Category, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(Category, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(isActive=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(isActive=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_ordered_by_price():
    if settings.LOW_CACHE:
        key = 'products_ordere  d_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(isActive=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(isActive=True).order_by('price')


def get_products_in_category_ordered_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_ordered_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, isActive=True). \
                order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, isActive=True). \
            order_by('price')

        # ===============================LOW CACHE=================================


def main_view(request):
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    products = Product.objects.all().select_related('category')
    trendy_products = TrendyProduct.objects.all().select_related('category')[:6]  # максимум 6 первых (чтобы не перегружать страницу)
    content = {
        'datetime': current_datetime,
        'date_text': current_date_text,
        'data': data,
        'products': products,
        'trendy': trendy_products,
        'basket': basket,
    }
    return render(request, 'index.html', content)


def contact_view(request):
    contact_cards = ContactCard.objects.all()
    return render(request, 'contact.html',
                  {'contact_card': contact_cards, 'datetime': current_datetime, 'date_text': current_date_text,
                   'data': data})


def get_hot_product():
    products = Product.objects.filter(isActive=True)[:6]  # ограничение для количества Trendy на странице (6)
    return products

def get_new_product():
    new_product = Product.objects.filter(isNew=True)[:6]
    return new_product



#@cache_page(3600)  # также замораживает Горячее предложение на 3600 сек
def products_view(request, pk=None, page=1):
    new_products = get_new_product()
    basket = []
    products = Product.objects.all().select_related('category')[:9]
    title = 'продукты'
    links_menu = get_links_menu()
    hot_product = random.sample(list(Product.objects.filter(isActive=True)), 1)[0]  # ТОТ самый рандомайзер
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    if pk:
        if pk is None:
            products = Product.objects.all().order_by('price')
            category = {'name': 'All'}
        else:
            category = get_object_or_404(Category, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')[:6]

        paginator = Paginator(products, 2)
        try:
            # получение объектов нужной страницы
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            # последняя страница
            products_paginator = paginator.page(paginator.num_pages)

        content = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': products,
            'datetime': current_datetime,
            'date_text': current_date_text,
            'data': data,  # JSON
            'new_products': new_products,
            'basket': basket,
            'hot_product': hot_product,
            'pk': pk,
        }
        return render(request, 'products.html', content)
    content = {
        'title': title,
        'links_menu': links_menu,
        'datetime': current_datetime,
        'date_text': current_date_text,
        'data': data,  # JSON
        'products': products,
        'new_products': new_products,
        'basket': basket,
        'hot_product': hot_product,
    }
    return render(request, 'products.html', content)
