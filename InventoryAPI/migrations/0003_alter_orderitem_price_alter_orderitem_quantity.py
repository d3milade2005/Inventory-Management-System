# Generated by Django 5.1.4 on 2024-12-22 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InventoryAPI', '0002_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.PositiveIntegerField(null=True),
        ),
    ]