# Generated by Django 4.2.7 on 2024-04-12 03:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_alter_orderdetail_req_id'),
        ('requirements', '0029_merge_20240412_0834'),
    ]

    operations = [
        migrations.AddField(
            model_name='requirementdetail',
            name='box_number',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='requirementcust',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.customerdetail'),
        ),
    ]
