import ordersapp.views as ordersapp
from django.urls import re_path, path

app_name = "ordersapp"

urlpatterns = [
    # TODO: path
    path('', ordersapp.OrderList.as_view(), name='orders_list'),
    # re_path(r'^$', ordersapp.OrderList.as_view(), name='orders_list'),
    re_path(r'^forming/complete/(?P<pk>\d+)/$', ordersapp.order_forming_complete, name='order_forming_complete'),

    re_path(r'^create/$', ordersapp.OrderItemsCreate.as_view(), name='order_create'),
    path('read/<int:pk>/', ordersapp.OrderRead.as_view(), name='order_read'),
    # re_path(r'^read/(?P<pk>\d+)/$', ordersapp.OrderRead.as_view(), name='order_read'),
    re_path(r'^update/(?P<pk>\d+)/$', ordersapp.OrderItemsUpdate.as_view(), name='order_update'),

    path('delete/<int:pk>/', ordersapp.OrderDelete.as_view(), name='order_delete'),
    # re_path(r'^delete/(?P<pk>\d+)/$', ordersapp.OrderDelete.as_view(), name='order_delete'),
]