
from django.views.generic import FormView
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .forms import LoginCredentialForm, LoginKeyForm
from .models import SecretKey
import logging

logger_debug_one = logging.getLogger("debug_one")


class LoginCredentialView(FormView):
    """
    По GET отображает форму для ввода имени и пароля пользователя.
    По POST генерирует и отправляет на почту одноразовый код и затем
    перенаправляет на ввод этого кода.
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
            new_secret_key = SecretKey.new_secret_key(user=user)
            send_mail(
                subject='Login to Fun board',
                message=f'Для входа используйте ключ: {new_secret_key}',
                from_email='',
                recipient_list=[user.email],
                fail_silently=False,
            )
            logger_debug_one.info(f'Login: send secret key {username}.')
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
        right_key = str(SecretKey.get_last_secret_key(user))
        if key == right_key:
            logger_debug_one.info(f'Login: check key. key is valid for {user} in {key} right {right_key}')
            login(request=request, user=user)
        else:
            logger_debug_one.info(f'Check key. INVALID for {user} in {key} right {right_key}')
        return redirect('/posts')


