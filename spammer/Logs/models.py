from django.db import models

from SetSending.models import SetSending
from spammer.settings import NULLABLE


class Logs(models.Model):
    time = models.DateTimeField(auto_now_add=True, verbose_name="время последней попытки")
    job = models.ForeignKey(SetSending, on_delete=models.CASCADE, verbose_name='Рассылка')
    status = models.SmallIntegerField(default=0, verbose_name="статус попытки")
    description = models.TextField(verbose_name="ответ почтового сервера", **NULLABLE)

    def __str__(self):
        return f"{self.time} - ({self.status}): {self.description}"

    class Meta:
        verbose_name = "Log"
