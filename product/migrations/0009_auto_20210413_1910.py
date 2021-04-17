# Generated by Django 3.1.7 on 2021-04-13 13:40

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_auto_20210413_1836'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tax',
            name='TaxPercentage',
        ),
        migrations.AlterField(
            model_name='product',
            name='createDate',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 13, 19, 10, 7, 456851)),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='createDate',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 13, 19, 10, 7, 456851)),
        ),
        migrations.AlterField(
            model_name='productclass',
            name='createDate',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 13, 19, 10, 7, 456851)),
        ),
        migrations.CreateModel(
            name='TaxSlab',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TaxPercentage', models.IntegerField(default=0, max_length=2)),
                ('isActive', models.BooleanField(default=True)),
                ('createdBy', models.CharField(max_length=200)),
                ('createDate', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('modifiedBy', models.CharField(blank=True, max_length=200, null=True)),
                ('modifiedDate', models.DateTimeField(blank=True, null=True)),
                ('TaxType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.tax')),
            ],
        ),
    ]
