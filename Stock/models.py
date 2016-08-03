from __future__ import unicode_literals

from django.db import models


# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=255, unique=True)
    identifier = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    @staticmethod
    def save_stock(stock_data):

        stock = Item()
        for k,v in stock_data.items():
            if (v == ''):
                raise EmptyValueException({"error_message": "Please enter all the values properly"})

        stock.name = stock_data['stock_name']
        stock.identifier = stock_data['stock_identifier']
        stock.company = stock_data['stock_company']

        return stock


class IncomingItem(models.Model):
    code = models.ForeignKey('Item', on_delete=models.CASCADE,
                             related_name='+')
    quantity = models.FloatField()
    rate = models.FloatField()
    amount = models.FloatField()
    received_from = models.CharField(max_length=200)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    @staticmethod
    def save_stock(data):

        item = IncomingItem()
        for k, v in data.items():
            print k
            if (v == ''):
                raise EmptyValueException({"error_message": "Please enter all the values properly"})

        item.code = Item.objects.get(pk = data['code'])
        item.quantity = data['quantity']
        item.rate = data['rate']
        item.amount = data['amount']
        item.received_from = data['received_from']

        return item


class DispatchingItem(models.Model):
    code = models.ForeignKey('Item', on_delete=models.CASCADE,
                             related_name='+')
    quantity = models.FloatField()
    rate = models.FloatField()
    amount = models.FloatField()
    comment = models.TextField()
    dispatched_to = models.CharField(max_length=255)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    @staticmethod
    def dispatch(data):

        item = DispatchingItem()
        for k, v in data.items():
            if (v == ''):
                raise EmptyValueException({"error_message": "Please enter all the values properly"})

        item.code = Item.objects.get(pk=data['code'])
        item.quantity = data['quantity']
        item.rate = data['rate']
        item.amount = data['amount']
        item.comment = data['comment']
        item.dispatched_to = data['dispatched_to']

        return item


class ReturningItem(models.Model):
    code = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='+')
    quantity = models.FloatField()
    returned_by = models.CharField(max_length=100)
    comment = models.TextField()
    damaged = models.BooleanField(default=False)
    date = models.DateField(auto_now=True)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    @staticmethod
    def returned(data):

        item = ReturningItem()
        for k, v in data.items():
            if (v == ''):
                raise EmptyValueException({"error_message": "Please enter all the values properly"})

        item.code = Item.objects.get(pk=data['code'])
        item.quantity = data['quantity']
        item.returned_by = data['returned_by']
        item.comment = data['comment']
        item.damaged = data['damaged']

        return item


class EmptyValueException(Exception):
    pass
