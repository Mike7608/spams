import os
import re
from datetime import datetime
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from django.core.management import BaseCommand
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from SetSending.models import SetSending
from message.models import Message
from django.core.mail import send_mail
from spammer.settings import EMAIL_HOST_USER

logger = logging.getLogger(__name__)

LAUNCHED = os.getenv('SPAM_LAUNCHED')


def send_email(email: Message, set_send: SetSending):
    list_address = re.split(pattern=";|,|\n", string=set_send.list_address)
    send_mail(email.subject, email.message, EMAIL_HOST_USER, list_address)


def my_job():
    set_send = SetSending.objects.filter(status=LAUNCHED)
    for item in set_send:
        if item.time_start <= datetime.now() < item.time_end:
            send_email(item.message, item)


# Декоратор close_old_connections гарантирует, что соединения с базой данных, которые стали
# непригодны для использования или устарели, закрываются до и после выполнения задания. Вы должны использовать это
# чтобы обернуть любые запланированные вами задания, которые каким-либо образом обращаются к базе данных Django.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    Это задание удаляет из базы данных записи выполнения заданий APScheduler старше max_age.
    Это помогает предотвратить заполнение базы данных старыми историческими записями, которые не являются
    дольше полезно.

    :param max_age: Максимальный срок хранения истории записей выполнения заданий.
                    По умолчанию 7 дней.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Запуск APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")

        set_send = SetSending.objects.filter(status=LAUNCHED)

        for item in set_send:
            scheduler.add_job(my_job, trigger=IntervalTrigger(seconds=item.interval, start_date=item.time_start,
                                                              end_date=item.time_end), id=f"my_job_{item.pk}",
                              replace_existing=True)

            logger.info(f"Added job «my_job_{item.pk}».")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Полночь понедельника, перед началом следующей рабочей недели.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )

        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
