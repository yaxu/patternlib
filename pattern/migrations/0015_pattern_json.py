# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-30 22:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pattern', '0014_pattern_editnumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='pattern',
            name='json',
            field=models.TextField(null=True),
        ),
    ]
