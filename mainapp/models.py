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
    SlideNo = models.PositiveIntegerField(verbose_name='Номер слайда в карусели верхнего слайдера', null=True, blank=True)
    isHot = models.BooleanField(verbose_name='Горячее предложение?', default=False)
    imageHot = models.ImageField(verbose_name='Картинка должна быть 1366х800 px', upload_to='products_hot', null=True, blank=True)
    SlideHotNo = models.PositiveIntegerField(verbose_name='Номер слайда в карусели "HOT"', null=True, blank=True)
    isNew = models.BooleanField(verbose_name='Поместить товар в раздел "новое"?', default=False)
    quantity = models.PositiveIntegerField(verbose_name='Количество на складе', default=1)
    isActive = models.BooleanField(verbose_name='Категория активна', default=True)

    @staticmethod #  статический метод - метод, к которому можно обращаться не через экземпляр класса, а через сам класс
    def get_items():
        return Product.objects.filter(isActive = True).order_by('category', 'name')

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
