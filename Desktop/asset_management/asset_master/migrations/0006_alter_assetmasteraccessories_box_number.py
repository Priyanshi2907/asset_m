# Generated by Django 4.2.7 on 2024-04-10 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset_master', '0005_alter_assetmasteraccessories_box_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetmasteraccessories',
            name='box_number',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]
