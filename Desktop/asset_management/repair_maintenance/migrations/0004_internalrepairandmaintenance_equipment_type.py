# Generated by Django 4.2.7 on 2024-02-05 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repair_maintenance', '0003_internalrepairandmaintenance_job_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='internalrepairandmaintenance',
            name='equipment_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]