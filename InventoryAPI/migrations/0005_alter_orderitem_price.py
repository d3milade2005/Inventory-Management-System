# Generated by Django 5.1.4 on 2024-12-22 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InventoryAPI', '0004_alter_orderitem_price_alter_orderitem_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10),
        ),
    ]