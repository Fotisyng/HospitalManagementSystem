# Generated by Django 5.1.1 on 2024-10-03 16:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('addresses', '0003_country'),
        ('emergency_contacts', '0003_alter_emergencycontact_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nurse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('date_of_birth', models.DateField()),
                ('phone_number', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('license_number', models.CharField(max_length=100, unique=True)),
                ('department', models.CharField(blank=True, max_length=50, null=True)),
                ('role', models.CharField(choices=[('staff', 'Staff Nurse'), ('charge', 'Charge Nurse'), ('chief', 'Chief Nurse')], default='staff', max_length=10)),
                ('date_hired', models.DateField()),
                ('hiring_end_date', models.DateField(blank=True, null=True)),
                ('address', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='addresses.address')),
                ('emergency_contact', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nurse_contact', to='emergency_contacts.emergencycontact')),
                ('supervised_nurses', models.ManyToManyField(blank=True, related_name='supervised_by', to='nurses.nurse')),
            ],
            options={
                'db_table': 'nurses',
            },
        ),
    ]