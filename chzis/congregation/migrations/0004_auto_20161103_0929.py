# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-11-03 09:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('congregation', '0003_set_perms'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='congregationmember',
            options={'ordering': ['user'], 'permissions': (('can_manage', 'Can manage'),)},
        ),
    ]