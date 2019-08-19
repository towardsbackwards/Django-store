"""MartynovStore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import re

from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.conf.urls import url, include
from django.urls import path, re_path

import mainapp.views as mainapp

urlpatterns = [
    url(r'^$', mainapp.main_View),
    url(r'^', include('mainapp.urls', namespace='main')),
    url(r'^', include('authapp.urls', namespace='auth')),
    url(r'^standartadmin/', admin.site.urls),
    url(r'^basket/', include('basketapp.urls', namespace='basket')),
    url(r'^admin/', include('adminapp.urls', namespace='admins')),
    re_path(r'^order/', include('ordersapp.urls', namespace='ordersapp')),
    re_path(r'^auth/verify/google/oauth2/', include("social_django.urls", namespace="social")),
    re_path(r'^auth/verify/vk/oauth2/', include('social_django.urls', namespace='social')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

