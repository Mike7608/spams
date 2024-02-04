from datetime import datetime
import pytz
import tzlocal
import re
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django.contrib import messages
from django.core.mail import send_mail
from django_apscheduler.jobstores import DjangoJobStore
from Logs.models import Logs
from SetSending.models import SetSending
from message.models import Message
from spammer.settings import EMAIL_HOST_USER


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
    def send_email(item_s: SetSending):
        """
        Процедура отправки сообщения
        :param item_s: SetSending элемент
        """
        # Получаем письмо для рассылки
        email: Message = Message.objects.get(id=item_s.message.pk)

        # получаем список адресатов
        list_a = re.split(pattern=";|\r|\n", string=item_s.list_address)
        list_address = []

        # Чистим список адресатов от пустых значений
        for item_l in list_a:
            if len(item_l) > 0:
                list_address.append(item_l)

        # отправка писем только если есть адресаты
        if len(list_address) > 0:
            send_mail(email.subject, email.message, EMAIL_HOST_USER, list_address)
            log_row = Logs.objects.create(job=item_s, status=1, description='доставлено')
            log_row.save()

    def change_status(self, item_s):
        """
        Процедура смены статуса на Завершен если время рассылки вышло
        :param item_s: SetSending
        """
        #
        # В данной процедуре был глюк, пока не перегрузил комп, джанго не сохранял изменения
        #

        # Берем все рассылки текущего пользователя
        sets = SetSending.objects.filter(user_id=item_s.user_id)

        # проходим по всем запущенным позицим, и если время рассылки вышло, изменяем статус на Завершен
        for item in sets:
            s1 = SetSending.objects.get(id=item.pk)
            now_time: datetime = DateTimeNow.current_datetime()
            s_time_end: datetime = item.time_end

            if item.status == Status.Running:
                if s_time_end < now_time:
                    item.status = Status.Completed  # Смена статуса
                    item.save()

    def my_job(self, pk: str):
        # получаем экземпляр SetSending
        item = SetSending.objects.get(id=int(pk))
        # отправляем почту согласно данного экземпляра
        self.send_email(item)
        # изменяем статусы у законченных рассылок
        self.change_status(item)

    def add_job(self, request, dataset: SetSending):
        # процедура добавления задания рассылки
        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")
        scheduler.add_job(self.my_job, trigger=IntervalTrigger(seconds=dataset.interval, start_date=dataset.time_start,
                                                               end_date=dataset.time_end), id=f"my_job_{dataset.pk}",
                          replace_existing=True, args=[f'{dataset.pk}'])
        # Запускаем рассылку
        scheduler.start()
        messages.add_message(request, messages.WARNING, f'Задание #{dataset.pk} успешно запущено!')


class Status:
    """
    Статусы рассылки
    """
    Completed = 0
    Created = 1
    Running = 2

    rus_list = [{'value': 1, 'text': 'Создан'}, {'value': 2, 'text': 'Запущен'}, {'value': 0, 'text': 'Завершен'}]


class DateTimeNow:
    """
    Класс для полдучения текущей даты в текущй таймзоне
    """
    @staticmethod
    def current_datetime():
        # получем текущую таймзону
        local_timezone_key = tzlocal.get_localzone()
        # получем время
        local_timezone = pytz.timezone(local_timezone_key.key)

        # Добавление смещения к часовому поясу
        new_timezone = local_timezone.localize(datetime.now())
        return new_timezone

