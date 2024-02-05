from django.db import models

from clients.models import Client
from message.models import Message
from users.models import User


class SetSending(models.Model):
    time_start = models.DateTimeField(verbose_name="время начала рассылки")
    interval = models.PositiveIntegerField(default=0, verbose_name="интервал рассылки в секундах")
    time_end = models.DateTimeField(verbose_name="время окончания рассылки")
    status = models.PositiveSmallIntegerField(default=1, verbose_name="статус рассылки")
    client = models.ManyToManyField(Client)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="сообщение")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")

    def __str__(self):
        return (f"Старт: {self.time_start}, Интервал: {self.interval} (сек.), Окончание: {self.time_end}, "
                f"Статус: {self.status}")

    class Meta:
        verbose_name = "Настройка рассылки"
        verbose_name_plural = "Настройки рассылки"

