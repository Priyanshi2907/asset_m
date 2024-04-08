# Generated by Django 4.2.7 on 2024-04-07 03:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_rename_assetss_orderdetail_assets'),
        ('requirements', '0008_remove_requirementdetail_customer_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requirementdetail',
            name='customer',
        ),
        migrations.AddField(
            model_name='requirementdetail',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.customerdetail'),
        ),
    ]
