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
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.conf.urls import include
from django.urls import path, re_path
import debug_toolbar
import mainapp.views as mainapp

urlpatterns = [
    path('', mainapp.main_view),
    path('', include('mainapp.urls', namespace='main')),
    path('', include('authapp.urls', namespace='auth')),
    path('order/', include('ordersapp.urls', namespace='order')),
    path('standartadmin/', admin.site.urls),
    path('basket/', include('basketapp.urls', namespace='basket')),
    path('admin/', include('adminapp.urls', namespace='admins')),
    path('order/', include('ordersapp.urls', namespace='ordersapp')),
    path('auth/verify/google/oauth2/', include("social_django.urls", namespace="social")),
    path('auth/verify/vk/oauth2/', include('social_django.urls', namespace='social')),

]
if settings.DEBUG:
    urlpatterns += [re_path(r'^__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

