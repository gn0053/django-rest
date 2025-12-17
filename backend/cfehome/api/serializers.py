from rest_framework import serializers

class UserProductInlineSerializer(serializers.Serializer): #bad idea but owrks
    url = serializers.HyperlinkedIdentityField(
        view_name="product-detail",
        lookup_field="pk",
        read_only=True
    )
    title = serializers.CharField(read_only=True)

class UserPublicSerializer(serializers.Serializer): #nested data
    username = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    # other_products = serializers.SerializerMethodField(read_only=True)

    def get_other_products(self, obj): #get_<serializer_filed>
        user = obj
        my_products_qs = user.product_set.all()[:5]
        return UserProductInlineSerializer(my_products_qs, many=True, context=self.context).data