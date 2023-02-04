from celery import shared_task
import logging
from datetime import datetime, time, timedelta
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .models import PortalUser, Posts

logger_debug_one = logging.getLogger("debug_one")


@shared_task
def send_mail_to_subscriber():
    for portal_user in PortalUser.objects.all():
        today = datetime.now()
        # ToDo вынести check_period в функуию и вызывать здесь и в Celery
        # За сколько дней проверяем новости. Коррелирует с расписанием Celery
        check_period = 7
        start = datetime.combine(today - timedelta(days=check_period), time.max)
        finish = datetime.combine(today, time.min)
        posted_last_weeks = Posts.objects.filter(created__range=[start, finish])

        if posted_last_weeks:
            domain = settings.CURRENT_HOST

            logger_debug_one.info(f'send email to user {portal_user}')

            html_content = render_to_string(
                'post_subscribe_email.html',
                {
                    'posted': posted_last_weeks,
                    'domain': domain,
                }
            )
            msg = EmailMultiAlternatives(
                subject=f'News of last week',
                body='',
                from_email='',
                to=[portal_user.user.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        else:
            logger_debug_one.info(f'send email:  nothing to send')
