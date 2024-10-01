# Generated by Django 5.1.1 on 2024-09-09 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0002_alter_address_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('iso_alpha_2', models.CharField(max_length=2, unique=True)),
                ('iso_alpha_3', models.CharField(max_length=3, unique=True)),
            ],
            options={
                'db_table': 'countries',
            },
        ),
    ]
