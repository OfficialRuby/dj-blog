# Generated by Django 3.0.8 on 2020-08-23 02:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0015_auto_20200822_2059'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='content',
        ),
    ]
