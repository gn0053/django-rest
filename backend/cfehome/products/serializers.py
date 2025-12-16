from rest_framework import serializers, reverse

from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    my_discount = serializers.SerializerMethodField(read_only=True) #for enrichment and renaming model fileds
    #urls in response
    #<wrong way
    # url = serializers.SerializerMethodField(read_only=True)
    #wrong way>
    class Meta:
        model = Product
        fields = [
            # "url",
            "pk",
            "title",
            "content",
            "price",
            "sale_price",
            "my_discount",
        ]

    #urls in response
    
    def get_url(self, obj):
        #<wrong way
    #     return f"api/products/{obj.id}/"
        #wrong way>
        request = self.context.get("request")
        if request is not None:
            return reverse("", kwargs={"pk":obj.pk}, request=request)
        return request

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