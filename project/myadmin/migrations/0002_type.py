# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-22 09:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('pid', models.IntegerField(default=0)),
                ('path', models.CharField(max_length=255)),
            ],
        ),
    ]