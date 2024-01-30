from django.db import models
from spammer.settings import NULLABLE
from users.models import User


class Client(models.Model):
    email = models.EmailField(max_length=100, verbose_name="email адрес")
    name = models.CharField(max_length=150, verbose_name="ФИО")
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)
    user = models.ForeignKey(User,  on_delete=models.DO_NOTHING, verbose_name='Пользователь')

    def __str__(self):
        return f"{self.name} ({self.email})"

    class Meta:
        verbose_name = "Клиент рассылки"
        verbose_name_plural = "Клиенты рассылки"

