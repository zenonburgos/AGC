from django.urls import path, include
from django.contrib.auth import views as auth_views

from core.login.views import *

urlpatterns = [
    path('', LoginFormView.as_view(), name="login"),
    path('logout/', LogoutRedirectView.as_view(), name="logout"),
    path('reset/password/', ResetPasswordView.as_view(), name="reset_password"),
    path('change/password/<str:token>/', ChangePasswordView.as_view(), name='change_password'),
    path('social_auth', include('social_django.urls', namespace='social')),
    # path('logout/', LogoutView.as_view(next_page='login'), name="logout")
]
