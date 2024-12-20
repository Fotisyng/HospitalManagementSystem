# Generated by Django 5.1.1 on 2024-09-08 12:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('addresses', '0002_alter_address_table'),
        ('patients', '0004_remove_patient_primary_care_physician'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('specialty', models.CharField(choices=[('GP', 'General Practitioner'), ('Cardiologist', 'Cardiologist'), ('Neurologist', 'Neurologist'), ('Dermatologist', 'Dermatologist')], max_length=50)),
                ('phone_number', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('license_number', models.CharField(max_length=100, unique=True)),
                ('address', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='addresses.address')),
                ('patients', models.ManyToManyField(related_name='doctors', to='patients.patient')),
            ],
        ),
    ]
