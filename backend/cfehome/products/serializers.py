from rest_framework import serializers
from rest_framework.reverse import reverse

from api.serializers import UserPublicSerializer
from .models import Product
# from .validators import validate_title
from .validators import validate_title_no_hello, unique_product_title

class ProductInlineSerializer(serializers.Serializer): #bad idea but owrks
    url = serializers.HyperlinkedIdentityField(
        view_name="product-detail",
        lookup_field="pk",
        read_only=True
    )
    title = serializers.CharField(read_only=True)

class ProductSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(source="user", read_only=True)
    # related_products = ProductInlineSerializer(source="user.product_set.all", read_only=True, many=True)
    # user_data = serializers.SerializerMethodField(read_only=True)
    my_discount = serializers.SerializerMethodField(read_only=True) #for enrichment and renaming model fileds
    #urls in response
    # edit_url = serializers.SerializerMethodField(read_only=True)

    #preffered url
    # url = serializers.HyperlinkedIdentityField(
    #     view_name="product-detail",
    #     lookup_field="pk",
    # )

    #non model field
    # email = serializers.EmailField(write_only=True)

    #adding validators via validators.py
    # title = serializers.CharField(validators=[
    #         validate_title_no_hello,
    #         unique_product_title,
    #     ])
    
    # name = serializers.CharField(source="title", read_only=True) #rename field, can use fkey relation ie user.email
    body = serializers.CharField(source="content", read_only=False)
    class Meta:
        model = Product
        # fields = [
        #     # "user",
        #     "owner",
        #     # "related_products",
        #     # "user_data",
        #     "url",
        #     "edit_url",
        #     "pk",
        #     "title",
        #     # "name",
        #     "body",
        #     "price",
        #     "sale_price",
        #     "my_discount",
        #     "public",
        #     "path",
        #     # "email",
        # ]
        fields = [
            "owner",
            "pk",
            "title",
            "body",
            "price",
            "sale_price",
            "my_discount",
            "public",
            "path",
            "endpoint",
        ]
    
    def get_user_data(self, obj): #get_<serializer_field>
        return {
            "username": obj.user.username
        }
    #validators def validate_<fieldname> moved to validators.py
    
    # def validate_title(self, value):
          # <request context
          # request = self.content.get("request")
          # user = request.user
          # qs = Product.objects.filter(user=user, title__iexact=value)
          # request context>
    #     qs = Product.objects.filter(title__iexact=value)
    #     if qs.exists():
    #         raise serializers.ValidationError(f"'{value}' already exists")
    #     return value


    #non model field
    # def create(self, validated_date):
    #     email = validated_date.pop("email")
    #     # return Product.objects.create(**validate_data) OR
    #     return super().create(validated_date)
    
    #if instace exists, instead of create:
    # def update(self, instance, validated_date):
    #     email = validated_date.pop("email")
    #     return super().update(instance, validated_date)
    
    #urls in response
    
    # def get_url(self, obj):
    #     #<wrong way
    # #     return f"api/products/{obj.id}/"
    #     #wrong way>
    #     request = self.context.get("request")
    #     if request is not None:
    #         return reverse("product-detail", kwargs={"pk":obj.pk}, request=request)
    #     return request

    def get_edit_url(self, obj):
        #<wrong way
    #     return f"api/products/{obj.id}/"
        #wrong way>
        request = self.context.get("request")
        if request is not None:
            return reverse("product-edit", kwargs={"pk":obj.pk}, request=request)
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