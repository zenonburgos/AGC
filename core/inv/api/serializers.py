from rest_framework.serializers import ModelSerializer

from core.inv.models import Category, Product


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image']


class ProductSerializer(ModelSerializer):
    category_data = CategorySerializer(source='category', read_only=True)
    # category_data = CategorySerializer(source='category', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'code', 'name', 'slug', 'image', 'price', 'active', 'category', 'category_data']