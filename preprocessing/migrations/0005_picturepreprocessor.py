# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-01-22 18:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('preprocessing', '0004_auto_20190122_1519'),
    ]

    operations = [
        migrations.CreateModel(
            name='PicturePreprocessor',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('preprocessing.audiopreprocessor',),
        ),
    ]