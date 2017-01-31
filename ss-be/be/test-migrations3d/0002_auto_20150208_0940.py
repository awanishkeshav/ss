# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beapi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsumerTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.BigIntegerField()),
                ('updated', models.BigIntegerField()),
                ('consumerId', models.BigIntegerField(db_index=True)),
                ('tag', models.CharField(default=b'', max_length=255)),
            ],
            options={
                'ordering': ('created',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TxnTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.BigIntegerField()),
                ('updated', models.BigIntegerField()),
                ('txnId', models.BigIntegerField()),
                ('tagId', models.BigIntegerField()),
                ('tag', models.CharField(default=b'', max_length=255, db_index=True)),
            ],
            options={
                'ordering': ('created',),
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='consumeraccount',
            name='phoneNum',
            field=models.BigIntegerField(default=1, db_index=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='consumercard',
            name='accountId',
            field=models.BigIntegerField(db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='consumercard',
            name='consumerId',
            field=models.BigIntegerField(db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='consumerdevice',
            name='deviceToken',
            field=models.CharField(default=b'', max_length=255, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='consumerprefs',
            name='consumerId',
            field=models.BigIntegerField(db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='consumertxn',
            name='consumerId',
            field=models.BigIntegerField(db_index=True),
            preserve_default=True,
        ),
    ]
