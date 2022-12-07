from django.contrib import admin

from core.orders.models import Seller
from core.orders.models import Table
from core.orders.models import Order
from core.orders.models import Payment


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    pass


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['table', 'product', 'status', 'created_at']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'table', 'statusPayment', 'paymentType', 'created_at']
