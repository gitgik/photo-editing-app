# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-23 13:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0010_auto_20160323_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image_effect',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
