# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beapi', '0004_auto_20150210_1352'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumertxn',
            name='tags',
            field=models.ForeignKey(blank=True, to='beapi.ConsumerTag', null=True),
        ),
    ]
