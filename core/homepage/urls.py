from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView, name='store'),
    path('store/', views.IndexView, name='home.urls'),
    # path('<slug:category_slug>/', views.IndexView, name='products_by_category'),
    # path('<slug:group_slug>/', views.IndexView, name='products_by_group'),   
]