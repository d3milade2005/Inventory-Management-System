from django.urls import path
from .views import ProductList, SingleProductList, InventoryList, SingleInventoryList, OrderList, SingleOrderList, OrderItemList, SingleOrderItemList

urlpatterns = [
    path('api/product/', ProductList.as_view()),
    path('api/product/<int:pk>/', SingleProductList.as_view()),
    path('api/inventory/', InventoryList.as_view()),
    path('api/inventory/<int:pk>/', SingleInventoryList.as_view()),
    path('api/order/', OrderList.as_view()),
    path('api/order/<int:pk>/', SingleOrderList.as_view()),
    path('api/order/<int:order_id>/items/', OrderItemList.as_view()),
    path('api/order-item/', OrderItemList.as_view()),
    path('api/order-item/<int:pk>/', SingleOrderItemList.as_view()),
    # path('api/stock-alert/', StockAlert.as_view()),
    # path('api/stock-alert/<int:pk>/', SingleStockAlert.as_view()),
]