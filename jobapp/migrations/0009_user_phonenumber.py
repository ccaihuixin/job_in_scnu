# Generated by Django 3.1.2 on 2021-03-30 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0008_auto_20210326_2359'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phonenumber',
            field=models.CharField(max_length=11, null=True),
        ),
    ]
