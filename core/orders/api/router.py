from rest_framework.routers import DefaultRouter
from core.orders.api.views import PaymentApiViewSet, SellerApiViewSet, TableApiViewSet, OrderApiViewSet

router_seller = DefaultRouter()
router_table = DefaultRouter()
router_order = DefaultRouter()
router_payment = DefaultRouter()

router_seller.register(
    prefix='sellers', basename='sellers', viewset=SellerApiViewSet
)

router_table.register(
    prefix='tables', basename='tables', viewset=TableApiViewSet
)

router_payment.register(
    prefix='payments', basename='payments', viewset=PaymentApiViewSet
)

router_order.register(
    prefix='orders', basename='orders', viewset=OrderApiViewSet
)
