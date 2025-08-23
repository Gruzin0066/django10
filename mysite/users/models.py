from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True, verbose_name='Фото')
    phone = models.CharField(max_length=13, blank=True, null=True, unique=True, verbose_name='Телефон')
    date_birth = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='Адрес')

    #От ИИ
    is_verified = models.BooleanField(default=False, verbose_name='Подтверждён')
    verification_token = models.CharField(max_length=100, blank=True, null=True)
    token_created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'