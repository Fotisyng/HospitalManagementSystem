# Generated by Django 5.1.1 on 2024-11-12 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0006_doctor_date_hired_doctor_date_of_birth_and_more'),
        ('patients', '0007_patient_department_patient_room_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='patients',
            field=models.ManyToManyField(blank=True, related_name='doctors', to='patients.patient'),
        ),
    ]
