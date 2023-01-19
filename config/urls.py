from django.contrib import admin
from django.urls import path, include
from core.homepage.views import IndexView
from core.login.views import *

from core.user.api.router import router_user
from core.inv.api.router import router_category
from core.inv.api.router import router_product

from core.store import views as StoreViews

from core.orders.api.router import router_seller, router_table, router_order, router_payment

from django.conf import settings
from django.conf.urls.static import static

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="AGC - ApiDocs",
      default_version='v1',
      description="Documentación de la API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="znburgos@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)

urlpatterns = [
    path('', IndexView, name="index"),
    path('store/', include('core.store.urls')),
    path('login/', include('core.login.urls')),
    path('accounts/', include('core.accounts.urls')),
    path('admin/', admin.site.urls),
    path('inv/', include('core.inv.urls')),
    path('reports/', include('core.reports.urls')),
    path('user/', include('core.user.urls')),
    path('socialaccounts/', include('allauth.urls')),
    
    # ORDERS from eccommerce or store
    path('orders/', include('core.orders_store.urls')),

   # CART PAGE
   path('cart/', StoreViews.cart, name='cart'),    
    
    # path('api/', include('core.api.urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redocs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    path('api/', include('core.user.api.router')),
    path('api/', include(router_user.urls)),
    path('api/', include(router_category.urls)),
    path('api/', include(router_product.urls)),
    path('api/', include(router_seller.urls)),
    path('api/', include(router_table.urls)),
    path('api/', include(router_order.urls)),
    path('api/', include(router_payment.urls)),
]

urlpatterns += static(setting.MEDIA_URL, document_root=settings.MEDIA_ROOT)
