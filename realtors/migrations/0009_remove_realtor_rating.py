# Generated by Django 3.1 on 2023-11-21 03:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('realtors', '0008_realtor_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='realtor',
            name='rating',
        ),
    ]