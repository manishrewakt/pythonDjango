# Generated by Django 3.1.7 on 2021-03-31 15:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_auto_20210331_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productclass',
            name='createDate',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 31, 20, 37, 2, 724041)),
        ),
        migrations.AlterField(
            model_name='productclass',
            name='createdBy',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
