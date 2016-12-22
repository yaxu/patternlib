# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pattern', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pattern',
            name='history',
            field=models.TextField(null=True),
        ),
    ]
