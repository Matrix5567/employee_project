# Generated by Django 4.0.5 on 2022-06-24 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employeapp', '0017_rename_date_leave_date_or_time_remove_leave_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='leave',
            name='time',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
