# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-11 19:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Stock', '0002_dispatchingitem_incomingitem_returningitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='created_at',
            field=models.DateField(auto_now=True),
        ),
    ]
