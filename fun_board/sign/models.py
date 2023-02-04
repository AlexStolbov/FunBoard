from django.contrib.auth.models import User
from django.db import models
import logging
import random

logger_debug_one = logging.getLogger("debug_one")


class SecretKey(models.Model):
    """
    Хранит одноразовые ключи для входа на сайт.
    Один пароль на одного пользователя.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    secret_key = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_last_secret_key(user):
        """
        Возвращает последний действующий код для аутентификации пользователя
        """
        found = SecretKey.objects.filter(user=user)
        if found.exists():
            return found[0].secret_key
        else:
            return None

    @staticmethod
    def new_secret_key(user: User) -> int:
        """
        Очищает все ранее выданные ключи.
        Записывает новый ключ.
        """
        old_keys = SecretKey.objects.filter(user=user)
        logger_debug_one.info(f'old keys. {old_keys}')
        for old in old_keys:
            old.delete()
        new_secret_key = random.randint(0, 1000000)
        SecretKey(user=user, secret_key=new_secret_key).save()
        return new_secret_key
