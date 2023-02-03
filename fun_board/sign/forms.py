from django import forms


class LoginCredentialForm(forms.Form):

    username = forms.CharField(label="Имя")
    password = forms.CharField(label="Пароль")

    class Meta:
        fields = [
            'username',
            'password',
        ]


class LoginKeyForm(forms.Form):

    key = forms.CharField(label="Введите код")

    class Meta:
        fields = [
            'key',
        ]
