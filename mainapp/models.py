from django.db import models
from django.contrib.auth.models import User


# User.objects.all() - получить список всех пользователей

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)  # Category & Product должны быть связаны.
    # Картинка
    image = models.ImageField(upload_to='products', null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    # строковый тип
    name = models.CharField(max_length=32, unique=True)
    description = models.TextField(verbose_name='Описание')
    price = models.PositiveIntegerField(verbose_name='Цена')
    rating = models.PositiveIntegerField(verbose_name='Рейтинг', default=1)
    alt = models.CharField(max_length=255, verbose_name='Текст рисунка', default='Текст по умолчанию')
    # 1. 1 к 1 = в одной категории только 1 товар.
    # category = models.OneToOneField(Category)
    # 2. 1 к многим = в одной категории много товаров, но один товар только в одной категории
    category = models.ForeignKey(Category, on_delete=models.PROTECT)  # Выбираем эту, как наиболее простую.
    # Если понадобится - усложним 1 или 3й. Варианты при удалении:  CASCADE, SET_NULL, PROTECT Для автозаполнения
    # третьим аргументов в ForeignKey было null = True. после автозаполнения удалили и заново мигрировали модель 3.
    # Многое к многому = в одной категори много товаров, но и один товар может быть в нескольких категориях category
    # = models.ManyToManyField(Category)
    image = models.ImageField(upload_to='products', null=True, blank=True)
    isTrendy = models.BooleanField(verbose_name='Товар сейчас в тренде?', default=False)
    isTopSlider = models.BooleanField(verbose_name='Товар должен быть в верхнем слайдере?', default=False)
    SlideNo = models.PositiveIntegerField(verbose_name='Номер слайда в карусели', null=True, blank=True)
    isHot = models.BooleanField(verbose_name='Горячее предложение?', default=False)
    isNew = models.BooleanField(verbose_name='Поместить товар в раздел "новое"?', default=False)


    def __str__(self):
        return self.name

    def discount(self):
        discount = 10
        result = round(self.price * (1 - (discount / 100)), 2)
        return result


class TrendyProduct(models.Model):
    name = models.CharField(max_length=32, unique=True)
    description = models.TextField(verbose_name='Описание')
    price = models.PositiveIntegerField(verbose_name='Цена')
    rating = models.PositiveIntegerField(verbose_name='Рейтинг', default=1)
    alt = models.CharField(max_length=255, verbose_name='Текст рисунка', default='Текст по умолчанию')
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    image = models.ImageField(upload_to='Trendy_products', null=True, blank=True)

    def __str__(self):
        return self.name

    def discount(self):
        discount = 10
        result = round(self.price * (1 - (discount / 100)), 2)
        return result


class ContactCard(models.Model):
    name = models.CharField(max_length=32)
    city = models.CharField(max_length=255, verbose_name='Город', default='Город не указан')
    phone = models.CharField(max_length=255, verbose_name='Номер телефона',
                             default='Номер не указан')  # charfield для того, чтобы указывать номер с дефисами
    email = models.CharField(max_length=255, verbose_name='Электронная почта', default='Эдектронная почта не указана')
    address = models.CharField(max_length=455, verbose_name='Адрес', default='Адрес не указан')

    def __str__(self):
        return self.name





class HotSliderProduct(models.Model):
    slideclass = models.CharField(max_length=155, verbose_name='Класс слайда', default='slides_hot slide1_hot')
    divstyle = models.CharField(max_length=855, verbose_name='Inline-стиль', default='margin: auto')
    h3text = models.CharField(max_length=255, verbose_name='Большой заголовок типа товаров', default='HOT DEAL')
    h2text = models.CharField(max_length=255, verbose_name='Название товара', default='Product')
    ptext = models.CharField(max_length=855, verbose_name='Описание товара', default='Description')
    image = models.ImageField(verbose_name='Картинка товара', upload_to='Slider_products', null=True, blank=True)
    alt = models.CharField(max_length=855, verbose_name='Alt текст', default='Alt text')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    price = models.PositiveIntegerField(verbose_name='Цена')
    rating = models.PositiveIntegerField(verbose_name='Рейтинг', default=1)

    def __str__(self):
        return self.slideclass

    def discount(self):
        discount = 10
        result = self.price * (1 - (discount / 100))
        return result
    # # число
    # n = models.IntegerField(max_length = 5, unique = True)
    # # float
    # n = models.FloatField()
    # # boolean
    # n = models.BooleanField()
    # # text
    # n = models.TextField()
    # # datetime
    # n = models.DateField()
    # n = models.DateTimeField()
    # # link
    # n = models.URLField()
    # # image
    # n = models.ImageField()
    # n = models.FileField()
    # # byte
    # n = models.BlobField()
