# Generated by Django 4.2.5 on 2024-08-09 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_user', '0005_user_avatar_user_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='uploads/default.jpg', null=True, upload_to='avatars/'),
        ),
    ]
