from django.urls import path
from . import views

app_name = 'productsApp'

urlpatterns = [
    path('products/<str:product_name>/', views.products, name='products'),                   # 产品列表
    path('productDetail/id=<int:id>', views.product_detail, name='productDetail'),     # 产品详情
]
