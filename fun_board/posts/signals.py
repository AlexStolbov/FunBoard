import logging
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import PortalUser, Comments

logger_debug_one = logging.getLogger("debug_one")


@receiver(post_save, sender=User)
def create_portal_user(sender, instance, created, **kwargs):
    """
    Создает нового пользователя портала при записи пользователя сайта.
    Если такой пользователь уже существует, то ничего не делаем.
    """
    if not PortalUser.objects.filter(user=instance).exists():
        new_portal_user = PortalUser(user=instance)
        new_portal_user.save()
        logger_debug_one.info(f'Create new PortalUser for {instance}')


@receiver(post_save, sender=Comments)
def comment_notice(sender, instance, created, **kwargs):
    """
    Если комментарий был одобрен или удален,
    отправляет автору уведомление на почту.
    """
    if not created:
        if instance.send_approved_notice():
            logger_debug_one.info(f'approve send {instance} sender {sender}')
            instance.approved_notice_sended()

        if instance.send_deleted_notice():
            logger_debug_one.info(f'delete send {instance} sender {sender}')
            instance.delete_notice_sended()


