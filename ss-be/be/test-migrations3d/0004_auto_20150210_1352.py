# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beapi', '0003_auto_20150208_1017'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consumertxn',
            name='merchantId',
        ),
        migrations.AddField(
            model_name='consumertxn',
            name='merchant',
            field=models.ForeignKey(blank=True, to='beapi.Merchant', null=True),
        ),
        migrations.AlterField(
            model_name='txntag',
            name='tagId',
            field=models.BigIntegerField(db_index=True),
        ),
    ]
