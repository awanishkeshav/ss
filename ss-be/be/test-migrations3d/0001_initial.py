# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.BigIntegerField()),
                ('updated', models.BigIntegerField()),
                ('name', models.CharField(default=b'', max_length=100, blank=True)),
                ('email', models.EmailField(default=b'', max_length=100, blank=True)),
                ('phone', models.CharField(default=b'', max_length=100, blank=True)),
                ('status', models.SmallIntegerField(default=1)),
            ],
            options={
                'ordering': ('created',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Consumer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.BigIntegerField()),
                ('updated', models.BigIntegerField()),
                ('firstname', models.CharField(default=b'', max_length=100, blank=True)),
                ('lastname', models.CharField(default=b'', max_length=100, blank=True)),
                ('email', models.EmailField(default=b'', max_length=100, blank=True)),
                ('dob', models.BigIntegerField(default=0, blank=True)),
                ('status', models.SmallIntegerField(default=1)),
                ('lat', models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True)),
                ('lng', models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True)),
            ],
            options={
                'ordering': ('created',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ConsumerAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.BigIntegerField()),
                ('updated', models.BigIntegerField()),
                ('clientId', models.BigIntegerField(default=1, blank=True)),
                ('cardNum', models.CharField(default=b'', max_length=255, blank=True)),
                ('phoneNum', models.BigIntegerField(default=1, blank=True)),
                ('limit', models.DecimalField(max_digits=10, decimal_places=2)),
                ('avaialbleLimit', models.DecimalField(max_digits=10, decimal_places=2)),
                ('currOS', models.DecimalField(max_digits=10, decimal_places=2)),
                ('activationCode', models.CharField(default=b'xxx', max_length=255)),
                ('cardNetwork', models.CharField(default=b'Master', max_length=10)),
                ('cardType', models.CharField(default=b'CreditCard', max_length=20)),
                ('cardTitle', models.CharField(default=b'Classic Card', max_length=20)),
            ],
            options={
                'ordering': ('created',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ConsumerAgg',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.BigIntegerField()),
                ('updated', models.BigIntegerField()),
                ('consumerId', models.BigIntegerField()),
                ('cardNum', models.CharField(default=b'', max_length=255)),
                ('amtSpentSS', models.DecimalField(max_digits=10, decimal_places=2)),
                ('periodKey', models.CharField(default=b'', max_length=255)),
                ('categoryKey', models.CharField(default=b'', max_length=255)),
                ('txType', models.SmallIntegerField(default=1)),
                ('blockedCards', models.CharField(default=b'', max_length=4096, blank=True)),
                ('blockedMerchants', models.CharField(default=b'', max_length=4096, blank=True)),
            ],
            options={
                'ordering': ('created',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ConsumerCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('clientId', models.BigIntegerField(default=1, blank=True)),
                ('consumerId', models.BigIntegerField()),
                ('accountId', models.BigIntegerField()),
                ('cardNum', models.CharField(default=b'', max_length=255, blank=True)),
                ('limit', models.DecimalField(max_digits=10, decimal_places=2)),
                ('avaialbleLimit', models.DecimalField(max_digits=10, decimal_places=2)),
                ('currOS', models.DecimalField(max_digits=10, decimal_places=2)),
                ('amtSpentSS', models.DecimalField(default=0.0, max_digits=10, decimal_places=2)),
                ('cardNetwork', models.CharField(default=b'Master', max_length=10)),
                ('cardType', models.CharField(default=b'CreditCard', max_length=20)),
                ('cardTitle', models.CharField(default=b'Classic Card', max_length=20)),
                ('status', models.CharField(default=b'Active', max_length=10)),
                ('created', models.BigIntegerField()),
                ('updated', models.BigIntegerField()),
            ],
            options={
                'ordering': ('created',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ConsumerDevice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.BigIntegerField()),
                ('updated', models.BigIntegerField()),
                ('consumerId', models.BigIntegerField()),
                ('cardNum', models.CharField(default=b'', max_length=255, blank=True)),
                ('deviceType', models.SmallIntegerField(default=1, blank=True)),
                ('deviceSubType', models.SmallIntegerField(default=1, blank=True)),
                ('deviceToken', models.CharField(default=b'', max_length=255)),
                ('status', models.SmallIntegerField(default=1)),
            ],
            options={
                'ordering': ('created',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ConsumerMerchant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.BigIntegerField()),
                ('updated', models.BigIntegerField()),
                ('consumerId', models.BigIntegerField()),
                ('merchantId', models.BigIntegerField()),
                ('status', models.SmallIntegerField(default=1)),
                ('currentDistance', models.DecimalField(max_digits=10, decimal_places=2)),
            ],
            options={
                'ordering': ('created',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ConsumerPrefs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.BigIntegerField()),
                ('updated', models.BigIntegerField()),
                ('consumerId', models.BigIntegerField()),
                ('cardNum', models.CharField(default=b'', max_length=255)),
                ('periodKey', models.CharField(default=b'', max_length=255)),
                ('limit', models.DecimalField(max_digits=10, decimal_places=2)),
                ('categoryKey', models.CharField(default=b'', max_length=255)),
                ('txType', models.SmallIntegerField(default=1)),
                ('action', models.SmallIntegerField(default=1)),
            ],
            options={
                'ordering': ('created',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ConsumerTxn',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.BigIntegerField()),
                ('updated', models.BigIntegerField()),
                ('consumerId', models.BigIntegerField()),
                ('cardId', models.BigIntegerField()),
                ('clientId', models.BigIntegerField()),
                ('merchantId', models.BigIntegerField()),
                ('txDate', models.BigIntegerField()),
                ('cardNum', models.CharField(default=b'', max_length=255)),
                ('amtSpentSS', models.DecimalField(max_digits=10, decimal_places=2)),
                ('category', models.CharField(default=b'General', max_length=255)),
                ('txType', models.CharField(default=b'Online', max_length=255)),
            ],
            options={
                'ordering': ('created',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.BigIntegerField()),
                ('updated', models.BigIntegerField()),
                ('name', models.CharField(default=b'', max_length=100, blank=True)),
                ('email', models.EmailField(default=b'', max_length=100, blank=True)),
                ('status', models.SmallIntegerField(default=1)),
                ('lat', models.DecimalField(max_digits=10, decimal_places=2)),
                ('lng', models.DecimalField(max_digits=10, decimal_places=2)),
            ],
            options={
                'ordering': ('created',),
            },
            bases=(models.Model,),
        ),
    ]
