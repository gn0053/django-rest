# from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, permissions, viewsets#, authentication
from rest_framework.decorators import api_view
from rest_framework.response import Response

# from api.authentication import TokenAuthentication
from .models import Product
from .serializers import ProductSerializer
# from api.permissions import IsStaffEditorPermission
from api.mixins import StaffEditorPermissionMixin

class ProductLisCreatetAPiView(StaffEditorPermissionMixin, generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"
    # authentication_classes = [ No longer needed due to settings
    #     authentication.SessionAuthentication,
    #     TokenAuthentication,
        
    #     ]
    # permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]
    def perform_create(self, serializer):
        title = serializer.validated_data.get("title")
        content = serializer.validated_data.get("content")
        if content is None:
            content = title
        serializer.save(content=content)

# class DetailUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
    
class ProductDetailAPiView(StaffEditorPermissionMixin, generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"
    
class ProductDetailAPiView(StaffEditorPermissionMixin, generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"

class ProductUpdateAPIView(StaffEditorPermissionMixin, generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = "pk"
    
    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title
            serializer.save()

class ProductDestroyAPIView(StaffEditorPermissionMixin, generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = "pk"

    def perform_destroy(self, instance):
        super().perform_destroy(instance)

class GenericMixinsViews( #function instead of if
    StaffEditorPermissionMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView,
    ):
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"
    permission_classes = [permissions.IsAuthenticated]

    def get (self, request, *args, **kwrags):
        pk = kwrags.get("pk")
        if pk is not None:
            return self.retrieve(request, *args, **kwrags)
        return self.list(request, *args, **kwrags)
    
    def post(self, request, *args, **kwrags):
        return self.create(request, *args, **kwrags)

    def perform_create(self, serializer):
        # title = serializer.validated_data.get("title")
        content = serializer.validated_data.get("content")
        if content is None:
            content = "mixin test"
        serializer.save(content=content)

@api_view(["GET", "POST"])
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method
    if method == "GET":
        if pk is not None:
            # queryset = Product.objects.all(pk=pk)
            # if not queryset.exists():
            #     raise Http404

            obj = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(obj, many=False).data
            return Response(data)
        
        #list if no pk
        queryset = Product.objects.all()
        data = ProductSerializer(queryset, many=True).data
        return Response(data)

    elif method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.et('title')
            content = serializer.validated_data.et('content') or None
            if content is None:
                content = title
            serializer.save(content=content)
            return Response(serializer.data)
        return Response({"Invalid": "Invalid Data"}, status=400)
    
#Routers
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"

#Why routers are a no-go
class ProductGenericViewset( #limits end points
        viewsets.GenericViewSet,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
    ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"

#view set above can be granulated as such:
# prod_list_view =  ProductGenericViewset.view({'get':'list'})
# prod_detail_view =  ProductGenericViewset.view({'get':'retrieve'})
    