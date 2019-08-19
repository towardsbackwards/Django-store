from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import url, include
import mainapp.views as mainapp

app_name = 'mainapp' # название для приложения mainapp

# ссылки, которые относятся к mainapp

urlpatterns = [
    url(r'^contact/$', mainapp.contact_View, name='contact'),
    url(r'^products/$', mainapp.products_View, name='products'),
    url(r'^index/$', mainapp.main_View, name='index'),
    url(r'^products/(?P<pk>\d+)/$', mainapp.products_View, name='category')
    
]