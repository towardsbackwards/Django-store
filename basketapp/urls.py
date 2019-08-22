from django.conf.urls import url
from django.urls import path, re_path

import basketapp.views as basketapp

app_name = 'basketapp'

urlpatterns = [
    path('', basketapp.basket, name='view'),
    re_path('^add/(?P<pk>\d+)/$', basketapp.basket_add, name='add'),
    re_path(r'^remove/(?P<pk>\d+)/$', basketapp.basket_remove, name='remove'),

    re_path(r'^edit/(?P<pk>\d+)/(?P<quantity>\d+)/$', basketapp.basket_edit, name='edit'),
    re_path(r'^ajaxdelete/(?P<pk>\d+)/$', basketapp.basket_ajaxdelete, name='delete'),
]