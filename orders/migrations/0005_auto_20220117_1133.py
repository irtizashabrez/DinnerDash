# Generated by Django 3.2 on 2022-01-17 06:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0004_alter_item_photo'),
        ('orders', '0004_auto_20220117_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='item_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='items.item'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order'),
        ),
    ]
