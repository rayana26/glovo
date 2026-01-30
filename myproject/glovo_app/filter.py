from django_filters import FilterSet
from .models import Product

class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'store': ['exact'],
            'product_name': ['exact'],
            'product_description': ['exact'],
            'price':['gt', 'lt'],
        }