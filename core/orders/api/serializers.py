from rest_framework.serializers import ModelSerializer

from core.orders.models import Seller
from core.orders.models import Table
from core.orders.models import Order
from core.orders.models import Payment

from core.inv.api.serializers import ProductSerializer


class SellerSerializer(ModelSerializer):
    class Meta:
        model = Seller
        fields = ['id', 'number']
    

class TableSerializer(ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'number']


class PaymentSerializer(ModelSerializer):
    table_data = TableSerializer(source='table', read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'table', 'table_data', 'totalPayment', 'paymentType', 'statusPayment', 'created_at']


class OrderSerializer(ModelSerializer):
    product_data = ProductSerializer(source='product', read_only=True)
    table_data = TableSerializer(source='table', read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'status', 'table', 'table_data', 'product', 'product_data', 'close', 'created_at']