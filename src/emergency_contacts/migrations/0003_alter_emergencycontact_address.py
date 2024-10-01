# Generated by Django 5.1.1 on 2024-09-29 11:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0003_country'),
        ('emergency_contacts', '0002_alter_emergencycontact_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emergencycontact',
            name='address',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='addresses.address'),
        ),
    ]