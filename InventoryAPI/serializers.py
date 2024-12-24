from .models import Product, InventoryTransaction, Order, OrderItem, StockAlert
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    
class SingleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'quantity_in_stock']

class InventorySerializer(serializers.ModelSerializer):
    product = SingleProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True, source='product')
    class Meta:
        model = InventoryTransaction
        fields = ['id', 'product', 'product_id', 'quantity', 'transaction_type', 'transaction_date', 'transaction_cost', 'transaction_amount']

class OrderItemSerializer(serializers.ModelSerializer):
    product = SingleProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True, source='product')
    price = serializers.SerializerMethodField(method_name='total_price', read_only=True)
    # order_id = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(), write_only=True, source='order')  # Add this line
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price']
    
    def total_price(self, order_item : OrderItem):
        return order_item.quantity * order_item.product.price

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_amount = serializers.SerializerMethodField(method_name='total', read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'telephone_number', 'order_date', 'status', 'total_amount', 'items']
    
    def total(self, order:Order):
        total_amount = sum(item.quantity * item.product.price for item in order.items.all())
        return total_amount
    
    
class StockAlertSerializer(serializers.ModelSerializer):
    product = SingleProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True, source='product')
    class Meta:
        model = StockAlert
        fields = ['id', 'product', 'product_id', 'stock_level', 'alert_date']