from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls import url, include
import mainapp.views as mainapp

app_name = 'mainapp' # название для приложения mainapp

# ссылки, которые относятся к mainapp

urlpatterns = [
    path('contact/', mainapp.contact_View, name='contact'),
    path('products/', mainapp.products_View, name='products'),
    path('index/', mainapp.main_View, name='index'),
    path(r'^products/<int:pk>/$', mainapp.products_View, name='category')
]