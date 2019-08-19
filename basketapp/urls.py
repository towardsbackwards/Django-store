from django.conf.urls import url

import basketapp.views as basketapp

app_name = 'basketapp'

urlpatterns = [
    url(r'^$', basketapp.basket, name='view'),
    url(r'^add/(?P<pk>\d+)/$', basketapp.basket_add, name='add'),
    url(r'^remove/(?P<pk>\d+)/$', basketapp.basket_remove, name='remove'),

    url(r'^edit/(?P<pk>\d+)/(?P<quantity>\d+)/$', basketapp.basket_edit, name='edit'),
    url(r'^ajaxdelete/(?P<pk>\d+)/$', basketapp.basket_ajaxdelete, name='delete'),
]