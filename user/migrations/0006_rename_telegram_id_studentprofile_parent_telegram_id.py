# Generated by Django 4.2.3 on 2023-07-25 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_studentprofile_telegram_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentprofile',
            old_name='telegram_id',
            new_name='parent_telegram_id',
        ),
    ]