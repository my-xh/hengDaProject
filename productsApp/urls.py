from django.urls import path
from . import views

app_name = 'productsApp'

urlpatterns = [
    path('<str:product_name>/', views.products, name='products'),
    path('productDetail/<int:id>', views.product_detail, name='productDetail'),
]
