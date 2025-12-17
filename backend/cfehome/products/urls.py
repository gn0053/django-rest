from django.urls import path
from . import views 

urlpatterns = [
    path('products/<int:pk>/', views.ProductDetailAPiView.as_view(), name="product-detail"),
    path('mixins/products/<int:pk>/', views.GenericMixinsViews.as_view()),
    
    path('products/<int:pk>/update/', views.ProductUpdateAPIView.as_view(), name="product-edit"),
    path('products/<int:pk>/delete/', views.ProductDestroyAPIView.as_view()),
    
    path('products/', views.ProductLisCreatetAPiView.as_view(), name="product-list"),
    path('mixins/products/', views.GenericMixinsViews.as_view()),
    
    path('alt_products/<int:pk>/', views.product_alt_view),
    path('alt_products/', views.product_alt_view),
    
]
