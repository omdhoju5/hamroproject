# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-30 19:57
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Cheque', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cheque',
            name='created_at',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 4, 30, 19, 57, 10, 162000, tzinfo=utc)),
            preserve_default=False,
        ),
    ]