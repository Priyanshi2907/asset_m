# Generated by Django 4.2.7 on 2024-04-10 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requirements', '0024_alter_requirementdetail_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requirementdetail',
            name='box_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
