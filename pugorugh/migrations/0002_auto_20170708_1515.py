# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-07-08 19:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pugorugh', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='gender',
            field=models.CharField(choices=[('m', 'Male'), ('f', 'Female'), ('u', 'Unknown')], max_length=1),
        ),
        migrations.AlterField(
            model_name='dog',
            name='size',
            field=models.CharField(choices=[('s', 'Small'), ('m', 'Medium'), ('l', 'Large'), ('xl', 'Extra Large'), ('u', 'Unknown')], max_length=2),
        ),
        migrations.AlterField(
            model_name='userdog',
            name='status',
            field=models.CharField(choices=[('l', 'Liked'), ('d', 'Disliked')], max_length=2),
        ),
    ]
