# Generated by Django 4.2.3 on 2023-07-22 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordertestinfostudent',
            name='submitted',
            field=models.BooleanField(default=False),
        ),
    ]