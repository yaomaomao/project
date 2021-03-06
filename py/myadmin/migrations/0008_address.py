# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-29 11:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0007_auto_20180626_1622'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=11)),
                ('address', models.CharField(max_length=20)),
                ('xiangxi', models.CharField(max_length=50)),
                ('status', models.IntegerField(default=0)),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myadmin.Users')),
            ],
        ),
    ]
