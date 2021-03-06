# Generated by Django 3.1.7 on 2021-04-13 13:52

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_auto_20210413_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='taxSlab',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.taxslab'),
        ),
        migrations.AlterField(
            model_name='product',
            name='createDate',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 13, 19, 22, 44, 427208)),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='createDate',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 13, 19, 22, 44, 427208)),
        ),
        migrations.AlterField(
            model_name='productclass',
            name='createDate',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 13, 19, 22, 44, 427208)),
        ),
    ]
