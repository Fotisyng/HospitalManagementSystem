# Generated by Django 5.1.1 on 2024-11-03 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nurses', '0006_add_hiring_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nurse',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('Other', 'Other')], default='Other', max_length=10),
        ),
    ]