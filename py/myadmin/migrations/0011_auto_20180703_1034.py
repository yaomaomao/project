# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-03 10:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0010_orders_addtime'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'permissions': (('show_address', '查看地址管理'), ('insert_address', '添加地址'), ('edit_address', '修改地址'), ('del_address', '删除地址'))},
        ),
        migrations.AlterModelOptions(
            name='goods',
            options={'permissions': (('show_goods', '查看商品管理'), ('insert_goods', '添加商品'), ('edit_goods', '修改商品'), ('del_goods', '删除商品'))},
        ),
        migrations.AlterModelOptions(
            name='orders',
            options={'permissions': (('show_order', '查看订单管理'), ('insert_order', '添加订单'), ('edit_order', '修改订单'), ('del_order', '删除订单'))},
        ),
        migrations.AlterModelOptions(
            name='types',
            options={'permissions': (('show_types', '查看商品分类管理'), ('insert_types', '添加商品分类'), ('edit_types', '修改商品分类'), ('del_types', '删除商品分类'))},
        ),
        migrations.AlterModelOptions(
            name='users',
            options={'permissions': (('show_users', '查看会员管理'), ('insert_users', '添加会员'), ('edit_users', '修改会员'), ('del_users', '删除会员'))},
        ),
    ]
