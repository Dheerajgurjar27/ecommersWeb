# Generated by Django 5.0.2 on 2024-03-02 06:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_rename_frist_name_custmer_first_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Custmer',
        ),
    ]