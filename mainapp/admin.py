from django.contrib import admin
from .models import Product, Category, TrendyProduct, ContactCard, HotSliderProduct
from authapp.models import ShopUser
# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(TrendyProduct)
admin.site.register(ContactCard)
admin.site.register(ShopUser)
admin.site.register(HotSliderProduct)