from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name="cus_register"),
    path('login/', views.login, name="cus_login"),
    path('logout/', views.logout, name="cus_logout"),
    path('dashboard/', views.dashboard, name="cus_dashboard"),
    path('', views.dashboard, name="cus_dashboard"),

    path('activate/<uidb64>/<token>/', views.activate, name="activate"),
]
