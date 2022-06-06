from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField
from django.db.models.fields.related import ForeignKey
from django.shortcuts import redirect
from authentications.models import MyUser
from items.models import Item


ORDER_STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Paid', 'Paid'),
    ('Completed', 'Completed'),
    ('Cancelled', 'Cancelled'),
    ('Ordered', 'Ordered')
)


class Order(models.Model):
    user_id = models.ForeignKey(MyUser, on_delete=CASCADE, null=True)
    order_time = models.DateTimeField(
        auto_now_add=True)
    status_updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    status = models.CharField(
        max_length=60, choices=ORDER_STATUS_CHOICES, default='Pending')
    total = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return 'Order id: ' + str(self.id) + ' user :' + str(self.user_id) + ' Status:' + str(self.status)

    def get_id(self):
        return self.id

    def get_total(self):
        return self.total

    def set_total(self, value):
        self.total = value


class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=CASCADE)
    item_id = models.ForeignKey(Item, on_delete=CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.order_id) + ' Item_id: ' + str(self.item_id.title) + ' quantity: ' + str(self.quantity) + " Price:" + str(self.item_id.price * self.quantity)

    def get_item_total(self):
        return str(self.item_id.price * self.quantity)
