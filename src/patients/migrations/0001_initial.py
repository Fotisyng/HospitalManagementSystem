# Generated by Django 5.1.1 on 2024-09-08 12:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('addresses', '0001_initial'),
        ('emergency_contacts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('N/A', 'Not Applicable')], max_length=10)),
                ('phone_number', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('start_prescription_date', models.DateField(blank=True, null=True)),
                ('end_prescription_date', models.DateField(blank=True, null=True)),
                ('medical_history', models.TextField(blank=True, null=True)),
                ('insurance_provider', models.CharField(blank=True, max_length=100, null=True)),
                ('insurance_policy_number', models.CharField(blank=True, max_length=50, null=True)),
                ('last_visit_date', models.DateField(blank=True, null=True)),
                ('primary_care_physician', models.CharField(blank=True, max_length=100, null=True)),
                ('allergies', models.TextField(blank=True, null=True)),
                ('registration_date', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('archived', 'Archived')], default='active', max_length=10)),
                ('address', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='addresses.address')),
                ('emergency_contact', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patient_contact', to='emergency_contacts.emergencycontact')),
            ],
        ),
    ]
