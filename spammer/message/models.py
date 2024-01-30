from django.db import models
from users.models import User
from spammer.settings import NULLABLE


class Message(models.Model):
    subject = models.CharField(max_length=250, verbose_name="тема письма")
    message = models.TextField(verbose_name="текст письма", **NULLABLE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return f"{self.subject} - ({self.message})"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
