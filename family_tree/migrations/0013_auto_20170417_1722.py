# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-17 17:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('family_tree', '0012_auto_20160607_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='birth_year',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='person',
            name='hierarchy_score',
            field=models.IntegerField(default=100),
        ),
        migrations.AlterField(
            model_name='person',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AddIndex(
            model_name='person',
            index=models.Index(fields=['name'], name='family_tree_name_2c4a7d_idx'),
        ),
        migrations.AddIndex(
            model_name='person',
            index=models.Index(fields=['family'], name='family_tree_family__434f0b_idx'),
        ),
        migrations.AddIndex(
            model_name='person',
            index=models.Index(fields=['birth_year'], name='family_tree_birth_y_dbd497_idx'),
        ),
        migrations.AddIndex(
            model_name='person',
            index=models.Index(fields=['user'], name='family_tree_user_id_356884_idx'),
        ),
        migrations.AddIndex(
            model_name='person',
            index=models.Index(fields=['hierarchy_score'], name='family_tree_hierarc_6798ff_idx'),
        ),
        migrations.AddIndex(
            model_name='relation',
            index=models.Index(fields=['from_person'], name='family_tree_from_pe_d87274_idx'),
        ),
        migrations.AddIndex(
            model_name='relation',
            index=models.Index(fields=['to_person'], name='family_tree_to_pers_4886ad_idx'),
        ),
    ]
