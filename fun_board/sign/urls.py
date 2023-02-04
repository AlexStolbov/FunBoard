from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import SignUpView, LoginCredentialView, LoginKeyView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('credential/', LoginCredentialView.as_view(), name='login_credential'),
    path('credential/key/', LoginKeyView.as_view(), name='login_key'),
    path('logout/', LogoutView.as_view(template_name='logout.html'),
         name='logout')
]
