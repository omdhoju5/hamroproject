from __future__ import unicode_literals

from django.db import models

class Cheque(models.Model):
    number = models.CharField(max_length=50)
    date = models.DateField(auto_now=True)
    name = models.CharField(max_length=100)
    amount = models.FloatField()
    exchanged = models.BooleanField(default=False)
    remark = models.TextField()
    issued = models.BooleanField(default=False)
    brought_by = models.CharField(max_length=100, null=True)
    assigned_to = models.CharField(max_length=100)
    bank = models.CharField(max_length=200)
    bank_branch = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def save_cheque(cheque_data):

        cheque = Cheque()

        cheque.name = cheque_data['cheque_name']
        cheque.amount = cheque_data['cheque_amount']
        cheque.date = cheque_data['cheque_date']
        cheque.number = cheque_data['cheque_number']
        cheque.remark = cheque_data['cheque_remark']

        cheque.save()


# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)

