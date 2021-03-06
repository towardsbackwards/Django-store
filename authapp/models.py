from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from datetime import timedelta


# Create your models here.

class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='user_avatar', blank=True)
    age = models.PositiveIntegerField(verbose_name='Возраст', null=True, default=18)

    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=now() + timedelta(hours=48))

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True


class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'F'

    GENDER_CHOICES = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
    )

    user = models.OneToOneField(ShopUser, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    tagline = models.CharField(verbose_name='теги', max_length=128, blank=True)
    aboutMe = models.TextField(verbose_name='о себе', max_length=512, blank=True)
    gender = models.CharField(verbose_name='пол', max_length=1, choices=GENDER_CHOICES, blank=True)
    bdate = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name='дата рождения', null=True, blank=True)
    '''photo_max
    user_ids
    lang
    interests'''

    # КОГДА У НАС МОДЕЛЬ SHOPUSER СОХРАНЯЕТСЯ МЕТОДОМ POST - ВЫПОЛНЯЕТСЯ ЭТОТ СИГНАЛ (сохраняет ShopUserProfile тоже):
    @receiver(post_save, sender=ShopUser)  # 1 - событие, инициирующее сигнал, 2 - модель, которая сгенерировала сигнал
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)
            print('В модели отработано сохранение профиля пользователя 1')

    @receiver(post_save, sender=ShopUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.shopuserprofile.save()
        print('В модели отработано сохранение профиля пользователя 2')
# Способ сохранения профиля пользователя также можно прописать методом save в классе ShopUser (переопределение метода
# save в модели
