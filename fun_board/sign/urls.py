from django.urls import path, include
from .views import LoginCredentialView, LoginKeyView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('credential/', LoginCredentialView.as_view(), name='login_credential'),
    path('credential/key/', LoginKeyView.as_view(), name='login_key'),
    path('logout/', LogoutView.as_view(
        template_name='logout.html'),
         name='logout')
]
