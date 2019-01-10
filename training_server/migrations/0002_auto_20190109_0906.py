# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-01-09 09:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training_server', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='algorithmconfig',
            name='input_data_filename',
            field=models.CharField(default='merged_folds_training_x', help_text='Filename or path to the input data file originating from ml_data folder', max_length=256),
        ),
        migrations.AddField(
            model_name='algorithmconfig',
            name='labels_filename',
            field=models.CharField(default='merged_folds_training_y', help_text='Filename or path to the input data file originating from ml_data folder', max_length=256),
        ),
    ]
