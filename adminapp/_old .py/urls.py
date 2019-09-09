from django.urls import path
from django.conf.urls import url, include
from .views import *
import adminapp.views as adminapp

app_name = 'adminapp' # название для приложения mainapp

# ссылки, которые относятся к mainapp

urlpatterns = [
    path('', adminapp.admin_view, name='table'),
    #url(r'^detail/$', adminapp.product_detail_view, name='detail'),
    path('detail/<int:pk>/', adminapp.product_detail_view, name='detailed'),
]