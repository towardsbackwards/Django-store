from django.contrib import admin
from .models import Product, Category, TrendyProduct, ContactCard, TopSliderProduct, HotSliderProduct
from authapp.models import ShopUser
# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(TrendyProduct)
admin.site.register(ContactCard)
admin.site.register(ShopUser)
admin.site.register(TopSliderProduct)
admin.site.register(HotSliderProduct)