# Generated by Django 4.2.8 on 2023-12-11 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customerCmd', '0005_remove_reply_parent_reply'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customercmd',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='reply',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
