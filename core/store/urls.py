from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),

    # # CART PAGE
    # path('cart/', views.cart, name='cart'),
    
    # path('store/', views.store, name='store.urls'),
    path('<slug:category_slug>/', views.store, name='products_by_category'),
    
    # ADD TO CARTS
    path('add_to_cart_in_product_detail/<int:producto_id>/', views.add_to_cart_in_product_detail, name='add_to_cart_in_product_detail'),
    path('add_to_cart/<int:producto_id>/', views.add_to_cart, name='add_to_cart'),
    
    # DECREASE CART
    path('decrease_cart/<int:producto_id>/', views.decrease_cart, name='decrease_cart'),

    #DELETE CART ITEM
    path('delete_cart/<int:cart_id>', views.delete_cart, name='delete_cart'),

    path('<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    # path('<slug:group_slug>/', views.store, name='products_by_group'),
     
    
]