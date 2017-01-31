# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beapi', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='txntag',
            old_name='tagId',
            new_name='consumerTag',
        ),
        migrations.RenameField(
            model_name='txntag',
            old_name='txnId',
            new_name='consumerTxn',
        ),
        migrations.AlterField(
            model_name='consumertxn',
            name='tags',
            field=models.ManyToManyField(to='beapi.ConsumerTag', null=True, through='beapi.TxnTag', blank=True),
            preserve_default=True,
        ),
    ]
