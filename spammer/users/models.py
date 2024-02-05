from django.contrib.auth.models import AbstractUser
from django.db import models
from spammer.settings import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='страна', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        # 'Can block users" или "Может блокировать пользователей".
        permissions = [
            (
                'can_block_users',
                'Может блокировать пользователей'
            ),
            (
                'can_block_SetSending',
                'Может отключать рассылки'
            )
        ]