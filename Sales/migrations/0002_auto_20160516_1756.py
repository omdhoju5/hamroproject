# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-17 01:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Sales', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoicedetail',
            name='invoice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detail', to='Sales.Invoice'),
        ),
        migrations.AlterField(
            model_name='invoicedetail',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock', to='Stock.Item'),
        ),
    ]
