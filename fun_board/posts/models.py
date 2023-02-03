from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

from . import resources


# Create your models here.

class PortalUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} ({self.rating})'


class Posts(models.Model):
    author = models.ForeignKey(PortalUser, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=300)
    category = models.CharField(max_length=3,
                                choices=resources.POSTS_CATEGORIES,
                                default="")
    # WYSIWYG field
    content = models.TextField(default="")

    def __str__(self):
        return f'Post: {self.title} by {self.author}'


class Comments(models.Model):
    author = models.ForeignKey(PortalUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField(default="")
    approved = models.BooleanField(default=False)
    # Если истина, нужно отправить уведомление об одобрении отклика
    approved_notice = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    # Если истина, нужно отправить уведомление об удалении отклика
    deleted_notice = models.BooleanField(default=False)

    def __str__(self):
        return f'Comment ({self.id}) for {self.post.title} by {self.author})'

    def send_approved_notice(self):
        """
        Возвращает истину, если нужно отправить уведомление об одобрении
        """
        return self.approved_notice

    def approved_notice_sended(self):
        """
        Отмечает, что уведомление об одобрении отправлено
        """
        self.approved_notice = False
        self.save()

    def send_deleted_notice(self):
        """
        Возвращает истину, если нужно отправить уведомление об удалении
        """
        return self.deleted_notice

    def delete_notice_sended(self):
        """
        Отмечает, что уведомление об удалении отправлено
        """
        self.deleted_notice = False
        self.save()
