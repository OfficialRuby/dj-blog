# Generated by Django 3.0.8 on 2020-08-22 20:45

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0009_remove_post_comment_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='cke',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
