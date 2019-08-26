from django.urls import path
import mainapp.views as mainapp

app_name = 'mainapp' # название для приложения mainapp

# ссылки, которые относятся к mainapp

urlpatterns = [
    path('contact/', mainapp.contact_view, name='contact'),
    path('products/', mainapp.products_view, name='products'),
    path('index/', mainapp.main_view, name='index'),
    path('products/<int:pk>/', mainapp.products_view, name='category')
]