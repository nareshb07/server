# Generated by Django 4.2.5 on 2023-10-30 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0035_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
    ]