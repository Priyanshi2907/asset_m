# Generated by Django 4.2.7 on 2024-04-07 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requirements', '0010_alter_requirementdetail_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requirementdetail',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='requirementdetail',
            name='order_id',
        ),
        migrations.AddField(
            model_name='requirementdetail',
            name='r_customer',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
