# Generated by Django 4.2.3 on 2023-09-18 08:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_sms'),
        ('education', '0012_ordertestinfo_name_ordertestinfo_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordertestinfo',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.teacherprofile'),
        ),
        migrations.AlterField(
            model_name='ordertestinfoassignstudent',
            name='order_test_info',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='education.ordertestinfo'),
        ),
        migrations.AlterField(
            model_name='ordertestinfoassignstudent',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.studentprofile'),
        ),
        migrations.AlterField(
            model_name='ordertestpack',
            name='order_test_info',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='education.ordertestinfo'),
        ),
        migrations.AlterField(
            model_name='ordertestpack',
            name='test',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='education.test'),
        ),
        migrations.AlterField(
            model_name='ordertestpackresultsofstudent',
            name='order_test_info',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='education.ordertestinfo'),
        ),
        migrations.AlterField(
            model_name='ordertestpackresultsofstudent',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.teacherprofile'),
        ),
        migrations.AlterField(
            model_name='test',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.teacherprofile'),
        ),
    ]
