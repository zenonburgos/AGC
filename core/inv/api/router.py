from rest_framework.routers import DefaultRouter
from core.inv.api.views import CategoryApiViewSet, ProductApiViewSet

router_category = DefaultRouter()
router_product = DefaultRouter()

router_category.register(
    prefix='categories', basename='categories', viewset=CategoryApiViewSet  
)

router_product.register(
    prefix='products', basename='products', viewset=ProductApiViewSet  
)