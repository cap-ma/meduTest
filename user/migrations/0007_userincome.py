# Generated by Django 4.2.3 on 2023-07-27 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_rename_telegram_id_studentprofile_parent_telegram_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserIncome',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instagram', models.IntegerField()),
                ('facebook', models.IntegerField()),
                ('telegram', models.IntegerField()),
                ('friend', models.IntegerField()),
                ('leaflet', models.IntegerField()),
                ('other', models.IntegerField()),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.teacherprofile')),
            ],
        ),
    ]
