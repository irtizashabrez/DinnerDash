from django.forms import fields
from rest_framework import serializers
# from cloudinary.models import CloudinaryField
from .models import Item, Category
from django.core.validators import MinValueValidator


class CategorySerilizers(serializers.ModelSerializer):
    # category = serializers.StringRelatedField(many=True)
    class Meta:
        model = Category
        fields = '__all__'


class ItemSerilizers(serializers.ModelSerializer):

    class Meta:
        model = Item
        depth = 1
        fields = '__all__'
        # fields = ['id', 'title', 'price', 'status', 'photo', 'category'] 
# ITEM_STATUS_CHOICES = (
#     ('Available', 'Available'),
#     ('Retired', 'Retired')
# )


# class CategorySerilizers(serializers.Serializer):
#     category = serializers.CharField(max_length=50)

#     def __str__(self):
#         return self.category


# class ItemSerilizers(serializers.Serializer):
#     title = serializers.CharField(max_length=50)
#     description = serializers.CharField(max_length=250)
#     price = serializers.FloatField(
#         validators=[MinValueValidator(0.1)],
#     )
#     status = serializers.CharField(
#         max_length=30)
#     photo = CloudinaryField('image', null=True, blank=True,
#                             default='https://res.cloudinary.com/dweuirck0/image/upload/v1642502378/nmvg73wekwwfhcjidt6c.jpg')
#     category = serializers.ManyToManyField(CategorySerilizers)

#     def __str__(self):
#         return self.title
