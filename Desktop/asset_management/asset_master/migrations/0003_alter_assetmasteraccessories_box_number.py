# Generated by Django 4.2.7 on 2024-04-09 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset_master', '0002_assetmasteraccessories_assetmaster_mapping_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetmasteraccessories',
            name='box_number',
            field=models.IntegerField(blank=True, default='', null=True),
        ),
    ]