from django.views.generic import FormView
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .forms import LoginCredentialForm, LoginKeyForm
import logging

logger_debug_one = logging.getLogger("debug_one")


def get_last_secret_key(user):
    """
    Возвращает последний действующий код для аутентификации пользователя
    """
    return '123'


class LoginCredentialView(FormView):
    """
    По GET отображает форму для ввода имени и пароля пользователя.
    По POST отправляет на почту одноразовый код и перенаправляет на ввод этого
    кода.
    """
    form_class = LoginCredentialForm
    template_name = 'login_credential.html'

    def post(self, request, *args, **kwargs):

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is None:
            # для повторного ввода данных пользователя
            logger_debug_one.info(f'Login: bad users data. {username} {password}')
            target = redirect('/posts')
        else:
            logger_debug_one.info(f'Login: send secret key {username}.')
            secret_key = get_last_secret_key(user);
            # send_mail(
            #     'Key',
            #     f'{secret_key}',
            #     'from@example.com',
            #     ['to@example.com'],
            #     fail_silently=False,
            # )
            target = redirect(f'key/?username={username}')

        return target


class LoginKeyView(FormView):
    """
    GET принимает одноразовый пароль
    POST проверяет одноразовый пароль, если ок, авторизует пользователя.
    """
    form_class = LoginKeyForm
    template_name = 'login_key.html'

    def post(self, request, *args, **kwargs):
        key = request.POST['key']
        user = User.objects.get(username=request.GET.get('username'))
        if key == get_last_secret_key(user):
            logger_debug_one.info(f'Login: check key. key is valid for {user}')
            login(request=request, user=user)
        else:
            logger_debug_one.info(
                f'Login: check key. !!! key is invalid for {user}')
        return redirect('/posts')


