# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-25 16:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pattern', '0009_auto_20170425_0919'),
    ]

    operations = [
        migrations.AddField(
            model_name='pattern',
            name='loves',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
