# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-30 19:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pattern', '0013_auto_20170425_2254'),
    ]

    operations = [
        migrations.AddField(
            model_name='pattern',
            name='editNumber',
            field=models.IntegerField(default=0),
        ),
    ]
