from rest_framework import serializers

from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    my_discount = serializers.SerializerMethodField(read_only=True) #for enrichment and renaming model fileds
    class Meta:
        model = Product
        fields = [
            "title",
            "content",
            "price",
            "sale_price",
            "my_discount",
        ]

    def get_my_discount(self, obj): # get_<methodfield>
        if not hasattr(obj, "id"):
            return None
        
        if not isinstance(obj, Product):
            return None
        
        return obj.get_discount()
        # try:
        #     return obj.get_discount() #obj is model method
        # except:
        #     return None