# Generated by Django 4.2.3 on 2023-07-24 09:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0004_ordertestpackstudent_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordertestpack',
            name='created_at',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
