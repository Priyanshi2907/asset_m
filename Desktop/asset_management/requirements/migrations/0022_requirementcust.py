# Generated by Django 4.2.7 on 2024-04-11 19:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_rename_assetss_orderdetail_assets'),
        ('requirements', '0021_delete_requirementcust'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequirementCust',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('r_cust_id', models.CharField(blank=True, max_length=10, null=True)),
                ('r_order_startdate', models.DateField(blank=True, null=True)),
                ('r_order_depdate', models.DateField(blank=True, null=True)),
                ('r_order_enddate', models.DateField(blank=True, null=True)),
                ('r_order_loc', models.CharField(blank=True, max_length=1000, null=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.customerdetail')),
            ],
        ),
    ]
