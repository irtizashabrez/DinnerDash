# Generated by Django 3.2 on 2022-01-16 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='superuser',
            field=models.BooleanField(default=False),
        ),
    ]
