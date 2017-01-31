# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beapi', '0002_auto_20150208_0940'),
    ]

    operations = [
        migrations.AddField(
            model_name='txntag',
            name='cardId',
            field=models.BigIntegerField(default=1, db_index=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='txntag',
            name='txnId',
            field=models.BigIntegerField(db_index=True),
            preserve_default=True,
        ),
    ]
