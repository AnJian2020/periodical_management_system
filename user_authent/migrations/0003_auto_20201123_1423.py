# Generated by Django 3.1.2 on 2020-11-23 06:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_authent', '0002_auto_20201123_0138'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usermenumodel',
            old_name='parent_menu',
            new_name='child_menu',
        ),
    ]
