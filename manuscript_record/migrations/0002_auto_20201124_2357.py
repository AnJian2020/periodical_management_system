# Generated by Django 3.1.2 on 2020-11-24 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manuscript_record', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contributiontypemodel',
            old_name='contribution_type_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='subjectmodel',
            old_name='subject_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='trademodel',
            old_name='trade_id',
            new_name='id',
        ),
    ]
