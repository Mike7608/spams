from django.db import models

from message.models import Message
from users.models import User


class SetSending(models.Model):
    time = models.DateTimeField(verbose_name="время рассылки")
    interval = models.PositiveIntegerField(default=0, verbose_name="интервал рассылки в секундах")
    status = models.PositiveSmallIntegerField(default=1, verbose_name="статус рассылки")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="сообщение")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")

    def __str__(self):
        return f"Старт: {self.time}, Интервал: {self.interval} (сек.), Статус: {self.status}"

    class Meta:
        verbose_name = "Настройка рассылки"
        verbose_name_plural = "Настройки рассылки"
