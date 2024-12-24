from django.shortcuts import render
from .serializers import ProductSerializer, InventorySerializer, OrderSerializer, OrderItemSerializer, StockAlertSerializer
from .models import Product, InventoryTransaction, Order, OrderItem, StockAlert
from rest_framework import generics, status
from rest_framework.response import Response
# Create your views here.


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            quantity_in_stock = serializer.validated_data.get('quantity_in_stock')
            name = serializer.validated_data.get('name')
            product = Product.objects.filter(name=name).first()

            if product:
                product.quantity_in_stock += quantity_in_stock
                product.save()
                return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
            else:
                # Create a new product if it does not exist
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

class SingleProductList(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def update(self, request, *args, **kwargs):
        """
        Handle PUT or PATCH requests to update the product's details.
        """
        partial = kwargs.pop('partial', False)  # Check if the request is PATCH
        instance = self.get_object()  # Retrieve the specific product instance
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # Update the quantity_in_stock if provided
        if 'quantity_in_stock' in serializer.validated_data:
            additional_quantity = serializer.validated_data['quantity_in_stock']
            instance.quantity_in_stock += additional_quantity
            
        for attr, value in serializer.validated_data.items():
            if attr != 'quantity_in_stock':  # Don't update quantity_in_stock again
                setattr(instance, attr, value)
        instance.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class InventoryList(generics.ListCreateAPIView):
    queryset = InventoryTransaction.objects.all()
    serializer_class = InventorySerializer

class SingleInventoryList(generics.RetrieveUpdateDestroyAPIView):
    queryset = InventoryTransaction.objects.all()
    serializer_class = InventorySerializer

class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class SingleOrderList(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemList(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def create(self, request, *args, **kwargs):
        order_id = kwargs['order_id']
        order = Order.objects.get(id=order_id)

        order.items.all().delete()

        product_id = int(request.data.get('product_id'))
        quantity = int(request.data.get('quantity'))

        product = Product.objects.get(id=product_id)

        if product.quantity_in_stock < quantity:
            return Response({'error': f'Not enough stock for {product.name}. Only {product.quantity_in_stock} available.'}, status=status.HTTP_400_BAD_REQUEST)

        # Reduce the stock and save the product
        product.quantity_in_stock -= quantity
        product.save()

        order_item = OrderItem.objects.create(order=order, product=product, quantity=quantity)

        # Optionally, change the status based on some conditions
        if order.total_amount > 0:  # You can adjust this based on your logic
            order.status = 'completed'  # Default status
        order.save()

        return Response(OrderItemSerializer(order_item).data, status=status.HTTP_201_CREATED)

class SingleOrderItemList(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

# class StockAlert(generics.ListCreateAPIView):
#     queryset = StockAlert.objects.all()
#     serializer_class = StockAlertSerializer

# class SingleStockAlert(generics.RetrieveUpdateDestroyAPIView):
#     queryset = StockAlert.objects.all()
#     serializer_class = StockAlertSerializer