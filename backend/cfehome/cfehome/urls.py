"""
URL configuration for cfehome project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#<ROUTER TEST
from rest_framework.routers import DefaultRouter
from products.views import ProductViewSet, ProductGenericViewset
#ROUTER TEST>

from django.contrib import admin
from django.urls import path, include
#<ROUTER TEST
router1 = DefaultRouter()
router1.register("products-route-test", ProductViewSet, basename="products")
router2 = DefaultRouter()
router2.register("products-route-test", ProductGenericViewset, basename="products")
#ROUTER TEST>
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include("api.urls")),
    path('api/v1/', include("products.urls")),
    path('api/v1/products/search/', include("search.urls")),
    #<ROUTER TEST
    path('api/v2/', include(router1.urls)),
    path('api/v2/better/', include(router2.urls)),
    #ROUTER TEST>
]
