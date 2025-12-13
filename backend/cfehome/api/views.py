# import json
# from django.http import JsonResponse
from django.forms.models import model_to_dict
from products.models import Product #, HttpResponse -> string
from rest_framework.response import Response
from rest_framework.decorators import api_view
from products.serializers import ProductSerializer

@api_view(["GET", "POST"])
def api_home(request, *args, **kwargs):
    if request.method == "GET":
        instance = Product.objects.all().order_by("?").first()
        data = {}
        if instance:
            data = ProductSerializer(instance).data
        return Response(data)
    
    elif request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save() #instance created, methods can now be used
            return Response(serializer.data)
        return Response({"Invalid": "Missing data"}, status=400)

# @api_view(["GET"])
# def api_home(request, *args, **kwargs):
#     model_data = Product.objects.all().order_by("?").first()
#     data = {}
#     if model_data:
#       data = model_to_dict(model_data, fields=["id", "title", "sale_price"])
#     return Response(data)

# def api_home(request, *args, **kwargs):
    # model_data = Product.objects.all().order_by("?").first()
    # data = model_to_dict(model_data, fields=["id", "title"])
    # data = {} Manual
    # if model_data:
    #     data["id"] = model_data.id
    #     data["title"] = model_data.title
    #     data["content"] = model_data.content
    #     data["price"] = model_data.price
    # return JsonResponse(data)
# 
# def api_home(request, *args, **kwargs):
#     body = request.body
#     data = {}
#     try:
#         data = json.loads(body)
#     except:
#         pass
#     data["params"] = dict(request.GET)
#     data["headers"] = dict(request.headers)
#     data["content_type"] = request.content_type
#     return JsonResponse(data)