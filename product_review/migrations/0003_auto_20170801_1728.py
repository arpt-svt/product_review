# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-01 17:28
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_review', '0002_auto_20170801_0703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='rate',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(5)]),
        ),
    ]