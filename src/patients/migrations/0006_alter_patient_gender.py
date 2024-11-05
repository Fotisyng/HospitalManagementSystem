# Generated by Django 5.1.1 on 2024-11-03 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0005_alter_patient_first_name_alter_patient_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('Other', 'Other')], default='Other', max_length=10),
        ),
    ]
