# Generated by Django 4.0.5 on 2022-06-27 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employeapp', '0020_alter_leave_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
