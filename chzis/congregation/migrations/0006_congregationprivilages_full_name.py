# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-04 14:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('congregation', '0005_auto_20160204_1315'),
    ]

    operations = [
        migrations.AddField(
            model_name='congregationprivilages',
            name='full_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]