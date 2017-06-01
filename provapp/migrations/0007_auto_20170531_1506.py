# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-31 13:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provapp', '0006_auto_20160405_1235'),
    ]

    operations = [
        migrations.CreateModel(
            name='RaveObsids',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rave_obs_id', models.TextField(blank=True, db_column='RAVE_OBS_ID', null=True)),
                ('obsdate', models.TextField(blank=True, db_column='Obsdate', null=True)),
                ('fieldname', models.TextField(blank=True, db_column='FieldName', null=True)),
                ('platenumber', models.TextField(blank=True, db_column='PlateNumber', null=True)),
                ('fibernumber', models.TextField(blank=True, db_column='FiberNumber', null=True)),
                ('id_2mass', models.TextField(blank=True, db_column='ID_2MASS', null=True)),
                ('id_denis', models.TextField(blank=True, db_column='ID_DENIS', null=True)),
                ('obs_collection', models.CharField(blank=True, max_length=128, null=True)),
            ],
            options={
                'db_table': 'rave_obsids',
                'managed': False,
            },
        ),
        migrations.AlterField(
            model_name='entity',
            name='type',
            field=models.CharField(choices=[('prov:Collection', 'prov:Collection'), ('voprov:dataSet', 'voprov:ctalog')], max_length=128, null=True),
        ),
    ]
