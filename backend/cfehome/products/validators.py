from .models import Product
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
# validators def validate_<fieldname>

# def validate_title(value):
#     qs = Product.objects.filter(title__iexact=value)
#     if qs.exists():
#         raise serializers.ValidationError(f"'{value}' already exists")
#     return value

def validate_title_no_hello(value):
    if "test" in value.lower():
        raise serializers.ValidationError(f"'{value}' is not allowed")
unique_product_title = UniqueValidator(queryset=Product.objects.all(), lookup="iexact")