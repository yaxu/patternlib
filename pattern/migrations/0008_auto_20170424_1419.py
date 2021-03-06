# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-24 13:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pattern', '0007_identity_ident'),
    ]

    operations = [
        migrations.AddField(
            model_name='pattern',
            name='errorMessage',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pattern',
            name='status',
            field=models.CharField(choices=[(b'error', b'Error'), (b'editing', b'Editing'), (b'rendering', b'Rendering'), (b'pending', b'Pending'), (b'live', b'Live')], default='editing', max_length=10),
            preserve_default=False,
        ),
    ]
