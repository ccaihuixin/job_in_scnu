# Generated by Django 3.1.2 on 2020-11-22 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job_info',
            old_name='infomation',
            new_name='information',
        ),
    ]