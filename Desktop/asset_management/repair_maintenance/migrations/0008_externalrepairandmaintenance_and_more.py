# Generated by Django 4.2.7 on 2024-03-07 20:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asset_master', '0002_assetmasteraccessories_assetmaster_mapping_and_more'),
        ('repair_maintenance', '0007_alter_internalrepairandmaintenance_accessories_qty_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalRepairAndMaintenance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eqiupment_type', models.CharField(blank=True, max_length=100, null=True)),
                ('equipment_name', models.CharField(blank=True, max_length=100, null=True)),
                ('model_no', models.CharField(blank=True, max_length=100, null=True)),
                ('serial_no', models.CharField(blank=True, max_length=100, null=True)),
                ('part_no', models.CharField(blank=True, max_length=100, null=True)),
                ('quantity', models.CharField(blank=True, max_length=100, null=True)),
                ('accessories', models.CharField(blank=True, max_length=100, null=True)),
                ('accessories_qty', models.CharField(blank=True, max_length=100, null=True)),
                ('out_date', models.DateField(blank=True, default=None, null=True)),
                ('out_time', models.TimeField(blank=True, default=None, null=True)),
                ('equipment_last_report_date', models.DateField(blank=True, default=None, null=True)),
                ('equipment_last_report_fault', models.CharField(blank=True, max_length=100, null=True)),
                ('equipment_received_by', models.CharField(blank=True, max_length=100, null=True)),
                ('equipment_handed_over_by', models.CharField(blank=True, max_length=100, null=True)),
                ('equipment_handed_over_to', models.CharField(blank=True, max_length=100, null=True)),
                ('default_detected', models.CharField(blank=True, max_length=100, null=True)),
                ('last_service_date', models.DateField(blank=True, default=None, null=True)),
                ('upcoming_service_date', models.DateField(blank=True, default=None, null=True)),
                ('repaired', models.CharField(blank=True, max_length=100, null=True)),
                ('specification', models.CharField(blank=True, max_length=100, null=True)),
                ('reason', models.CharField(blank=True, max_length=100, null=True)),
                ('date_of_intimation', models.DateField(blank=True, default=None, null=True)),
                ('informed_contact_person', models.CharField(blank=True, max_length=100, null=True)),
                ('signature', models.CharField(blank=True, max_length=100, null=True)),
                ('equipment_collected_by', models.CharField(blank=True, max_length=100, null=True)),
                ('quantity_collected', models.CharField(blank=True, max_length=100, null=True)),
                ('date_of_collection', models.DateField(blank=True, default=None, null=True)),
                ('quantity_received', models.CharField(blank=True, max_length=100, null=True)),
                ('date_of_receipt', models.DateField(blank=True, default=None, null=True)),
                ('equipment_handed_to_eng_team', models.CharField(blank=True, max_length=100, null=True)),
                ('equipment_fitted_in_rack', models.CharField(blank=True, max_length=100, null=True)),
                ('asset_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asset_master.assetmaster')),
            ],
        ),
        migrations.AddField(
            model_name='internalrepairandmaintenance',
            name='equipment_handed_over_by_name_appt',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='internalrepairandmaintenance',
            name='equipment_handing_over_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='internalrepairandmaintenance',
            name='equipment_handing_over_signature',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='internalrepairandmaintenance',
            name='equipment_received_by_name_section',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='internalrepairandmaintenance',
            name='equipment_received_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='internalrepairandmaintenance',
            name='equipment_receiver_signature',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='internalrepairandmaintenance',
            name='equipment_repaired_by',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='internalrepairandmaintenance',
            name='marked_for_oem_date',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='internalrepairandmaintenance',
            name='repair_activity_completion_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='internalrepairandmaintenance',
            name='signature_of_engineering_head',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='media/'),
        ),
        migrations.AddField(
            model_name='internalrepairandmaintenance',
            name='signature_of_engineering_inventory_head',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='media/'),
        ),
        migrations.AddField(
            model_name='internalrepairandmaintenance',
            name='time_taken_to_repair',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.CreateModel(
            name='SparesInteranlRepair',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reqmt', models.CharField(blank=True, max_length=100, null=True)),
                ('quantity', models.CharField(blank=True, max_length=100, null=True)),
                ('date_of_demand_requisition', models.CharField(blank=True, max_length=100, null=True)),
                ('date_of_receipt', models.CharField(blank=True, max_length=100, null=True)),
                ('date_of_fitment', models.CharField(blank=True, max_length=100, null=True)),
                ('cost', models.CharField(blank=True, max_length=100, null=True)),
                ('spares_produced_through', models.CharField(blank=True, max_length=100, null=True)),
                ('procurement_sanctioned_by', models.CharField(blank=True, max_length=100, null=True)),
                ('signature', models.CharField(blank=True, max_length=100, null=True)),
                ('internal_repair_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repair_maintenance.internalrepairandmaintenance')),
            ],
        ),
        migrations.CreateModel(
            name='InternalRepairOutDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('equipment_repaired_by', models.CharField(blank=True, max_length=100, null=True)),
                ('repair_activity_completion_date', models.CharField(blank=True, max_length=100, null=True)),
                ('marked_for_oem_date', models.CharField(blank=True, max_length=100, null=True)),
                ('time_taken_to_repair', models.CharField(blank=True, max_length=100, null=True)),
                ('equipment_handed_over_by', models.CharField(blank=True, max_length=100, null=True)),
                ('equipment_handing_over_date', models.CharField(blank=True, max_length=100, null=True)),
                ('equipment_handing_over_signature', models.CharField(blank=True, max_length=100, null=True)),
                ('equipment_received_by', models.CharField(blank=True, max_length=100, null=True)),
                ('equipment_received_date', models.CharField(blank=True, max_length=100, null=True)),
                ('equipment_receiver_signature', models.CharField(blank=True, max_length=100, null=True)),
                ('internal_repair_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repair_maintenance.internalrepairandmaintenance')),
            ],
        ),
        migrations.CreateModel(
            name='InternalRepairComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(blank=True, max_length=100, null=True)),
                ('date_time', models.DateTimeField()),
                ('repair_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repair_maintenance.internalrepairandmaintenance')),
            ],
        ),
        migrations.CreateModel(
            name='InternalRepairAttachFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attached_file', models.FileField(blank=True, default=None, null=True, upload_to='media/')),
                ('repair_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repair_maintenance.internalrepairandmaintenance')),
            ],
        ),
        migrations.CreateModel(
            name='ExternalRepairComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(blank=True, max_length=100, null=True)),
                ('date_time', models.DateTimeField()),
                ('repair_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repair_maintenance.externalrepairandmaintenance')),
            ],
        ),
        migrations.CreateModel(
            name='ExternalRepairAttachFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attached_file', models.FileField(blank=True, default=None, null=True, upload_to='media/')),
                ('repair_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repair_maintenance.externalrepairandmaintenance')),
            ],
        ),
        migrations.CreateModel(
            name='ExternalEquipmentForwardDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('falut_reported', models.CharField(blank=True, max_length=100, null=True)),
                ('falut_detected', models.CharField(blank=True, max_length=100, null=True)),
                ('falut_occured', models.CharField(blank=True, max_length=100, null=True)),
                ('type_of_repair_carried_out', models.CharField(blank=True, max_length=100, null=True)),
                ('external_repair_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repair_maintenance.externalrepairandmaintenance')),
            ],
        ),
        migrations.CreateModel(
            name='ExternalAdvisoryForEquipmentHandling',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remarks', models.CharField(blank=True, max_length=100, null=True)),
                ('external_repair_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repair_maintenance.externalrepairandmaintenance')),
            ],
        ),
    ]