# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-17 17:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0012_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='language',
            field=models.CharField(choices=[('en', 'English'), ('zh-tw', 'Traditional Chinese'), ('zh-cn', 'Simplified Chinese'), ('pl', 'Polish'), ('fi', 'Finnish'), ('fr', 'French')], default='en', max_length=5),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['email'], name='custom_user_email_a0b6c8_idx'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['family'], name='custom_user_family__615fa8_idx'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['language'], name='custom_user_languag_612014_idx'),
        ),
    ]