# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-17 17:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emailer', '0009_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='recipient',
            field=models.EmailField(max_length=254),
        ),
        migrations.AddIndex(
            model_name='email',
            index=models.Index(fields=['recipient'], name='emailer_ema_recipie_4eb5cc_idx'),
        ),
    ]