# Generated by Django 4.2.7 on 2024-04-10 09:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('requirements', '0018_alter_requirementdetail_r_order_loc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requirementdetail',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='requirementdetail',
            name='r_order_depdate',
        ),
        migrations.RemoveField(
            model_name='requirementdetail',
            name='r_order_enddate',
        ),
        migrations.RemoveField(
            model_name='requirementdetail',
            name='r_order_loc',
        ),
        migrations.RemoveField(
            model_name='requirementdetail',
            name='r_order_startdate',
        ),
    ]
