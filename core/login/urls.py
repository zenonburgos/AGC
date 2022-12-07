from django.urls import path

from core.login.views import *

urlpatterns = [
    path('', LoginFormView.as_view(), name="login"),
    path('logout/', LogoutRedirectView.as_view(), name="logout"),
    path('reset/password/', ResetPasswordView.as_view(), name="reset_password"),
    path('change/password/<str:token>/', ChangePasswordView.as_view(), name='change_password')
    # path('logout/', LogoutView.as_view(next_page='login'), name="logout")
]
