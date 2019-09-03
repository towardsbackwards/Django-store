from django.contrib import admin

from ordersapp.models import Order
from ordersapp.views import OrderList
from .models import Product, Category, TrendyProduct, ContactCard
from authapp.models import ShopUser
# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(TrendyProduct)
admin.site.register(ContactCard)
admin.site.register(ShopUser)
admin.site.register(Order)