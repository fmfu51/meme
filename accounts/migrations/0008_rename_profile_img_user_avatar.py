# Generated by Django 3.2.9 on 2022-01-26 10:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_user_bio'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='profile_img',
            new_name='avatar',
        ),
    ]
