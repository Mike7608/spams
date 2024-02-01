from datetime import datetime
import re
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django.core.mail import send_mail
from django_apscheduler.jobstores import DjangoJobStore
from Logs.models import Logs
from SetSending.models import SetSending
from message.models import Message
from spammer.settings import EMAIL_HOST_USER, LIST_STATUS


class StyleFormMixin:
    """
    Миксин для стилизации формы
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class JobService:

    @staticmethod
    def send_email(email: Message, set_send: SetSending):
        list_address = re.split(pattern=";|,|\n", string=set_send.list_address)
        send_mail(email.subject, email.message, EMAIL_HOST_USER, list_address)
        log_row = Logs.objects.create(job=set_send, status=1, description='доставлено')
        log_row.save()

    def my_job(self):
        set_send = SetSending.objects.filter(status=LIST_STATUS[2])
        for item in set_send:
            if item.time_start <= datetime.now() < item.time_end:
                self.send_email(item.message, item)

    def add_job(self, time_start, time_end, interval, job_id):
        scheduler = BlockingScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(self.my_job, trigger=IntervalTrigger(seconds=interval, start_date=time_start,
                                                               end_date=time_end), id=f"my_job_{job_id}",
                          replace_existing=True)


