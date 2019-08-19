from django.conf.urls import url
from django.urls import re_path
import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    url(r'^login/$', authapp.login, name='login'),
    url(r'^logout/$', authapp.logout, name='logout'),
    url(r'^register/$', authapp.register, name='register'),
    url(r'^edit/$', authapp.edit, name='edit'),
    re_path(r'^verify/(?P<email>.+)/(?P<activation_key>\w+)/$', authapp.verify, name='verify'),
]