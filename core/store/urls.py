from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),

    # # CART PAGE
    # path('cart/', views.cart, name='cart'),
    
    # path('store/', views.store, name='store.urls'),
    path('categoria/<slug:category_slug>/', views.store, name='products_by_category'),
    path('categoria/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
   
    path('search/', views.search, name='search'),
    
    # ADD TO CARTS
    path('add_to_cart_in_product_detail/<int:producto_id>/', views.add_to_cart_in_product_detail, name='add_to_cart_in_product_detail'),
    path('add_to_cart/<int:producto_id>/', views.add_to_cart, name='add_to_cart'),
    
    # DECREASE CART
    path('decrease_cart/<int:producto_id>/', views.decrease_cart, name='decrease_cart'),

    #DELETE CART ITEM
    path('delete_cart/<int:cart_id>', views.delete_cart, name='delete_cart'),
    # path('<slug:group_slug>/', views.store, name='products_by_group'),
    
    path('checkout/', views.checkout, name='checkout'),
]