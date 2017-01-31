# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beapi', '0005_consumertxn_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='txntag',
            name='tag',
        ),
        migrations.AlterField(
            model_name='consumertxn',
            name='merchant',
            field=models.ForeignKey(related_name='merchantId', blank=True, to='beapi.Merchant', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='consumertxn',
            name='tags',
            field=models.ManyToManyField(to='beapi.ConsumerTag', through='beapi.TxnTag'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='txntag',
            name='tagId',
            field=models.ForeignKey(related_name='tagId', blank=b'False', to='beapi.ConsumerTag'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='txntag',
            name='txnId',
            field=models.ForeignKey(related_name='consumertxn_id', blank=b'False', to='beapi.ConsumerTxn'),
            preserve_default=True,
        ),
    ]
