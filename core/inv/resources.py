from import_export import resources
from inv.models import Product

class ProductResource(resources.ModelResource):
    class Meta:
        model: Product

