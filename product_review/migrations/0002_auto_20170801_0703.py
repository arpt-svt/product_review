# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-01 07:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_review', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='name',
        ),
        migrations.AddField(
            model_name='product',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
