# Generated by Django 4.2.3 on 2023-07-27 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_rename_userincome_usertraffic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertraffic',
            name='facebook',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='usertraffic',
            name='friend',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='usertraffic',
            name='instagram',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='usertraffic',
            name='leaflet',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='usertraffic',
            name='other',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='usertraffic',
            name='telegram',
            field=models.IntegerField(default=0),
        ),
    ]
