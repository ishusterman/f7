# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-03-25 04:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_f7', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='t_move',
            name='go_out_to_other_stac',
            field=models.PositiveIntegerField(default=0, verbose_name='Выписано в др. стационар'),
            preserve_default=False,
        ),
    ]
