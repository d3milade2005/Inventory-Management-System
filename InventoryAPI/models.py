from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    quantity_in_stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    threshold_level = models.PositiveIntegerField(default=5)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} | {self.price}"

class InventoryTransaction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=255) #restock, sold
    quantity = models.PositiveIntegerField() #number of items removed
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) #amount for purchaes
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) #amount for sale

    def __str__(self):
        return f"{self.transaction_type} | {self.transaction_cost}"

class Order(models.Model):
    customer_name = models.CharField(max_length=255)
    telephone_number = PhoneNumberField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, choices=[('pending', 'Pending'), ('completed', 'Completed')])
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True)

    def __str__(self):
        return f"{self.customer_name} | {self.total_amount}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.quantity} | {self.product.name}"

class StockAlert(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stock_level = models.PositiveIntegerField()
    alert_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.stock_level} | {self.alert_date}"