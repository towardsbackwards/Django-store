from django.conf.urls import url
from django.urls import path, re_path

import basketapp.views as basketapp

app_name = 'basketapp'

urlpatterns = [
    path('', basketapp.basket, name='view'),
    path('add/<int:pk>/', basketapp.basket_add, name='add'),
    path('remove/<int:pk>/', basketapp.basket_remove, name='remove'),

    re_path('^edit/(?P<pk>\d+)/(?P<quantity>\d+)/$', basketapp.basket_edit, name='edit'),
    path('ajaxdelete/<int:pk>/', basketapp.basket_ajaxdelete, name='delete'),
]