# Generated by Django 3.2 on 2022-01-10 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('Paid', 'Paid'), ('complete', 'Complete '), ('cancle', 'Cancle')], default='pending', max_length=60),
        ),
        migrations.AlterField(
            model_name='order',
            name='total',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]