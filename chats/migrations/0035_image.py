# Generated by Django 4.2.5 on 2023-09-28 15:34

from django.db import migrations, models
import storages.backends.s3boto3


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0034_alter_user_is_follower'),
    ]

    operations = [
        migrations.CreateModel(
            name='image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='Profile_Pictures/dp.png', storage=storages.backends.s3boto3.S3Boto3Storage(), upload_to='Profile_Pictures/')),
                ('image_name', models.CharField(null=True)),
            ],
        ),
    ]