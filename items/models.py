from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import OneToOneField
from cloudinary.models import CloudinaryField

ITEM_STATUS_CHOICES = (
    ('Available', 'Available'),
    ('Retired', 'Retired')
)


class Category(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category


class Item(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=250)
    price = models.FloatField(
        validators=[MinValueValidator(0.1)],
    )
    status = models.CharField(
        max_length=30, choices=ITEM_STATUS_CHOICES, default='Available')
    photo = CloudinaryField('image', null=True, blank=True,
                            default='https://res.cloudinary.com/dweuirck0/image/upload/v1642502378/nmvg73wekwwfhcjidt6c.jpg')
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.title
