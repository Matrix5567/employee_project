# Generated by Django 4.0.5 on 2022-06-27 08:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employeapp', '0025_rename_early_logout_late_comming_time_leave_date_or_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='leave',
            old_name='date_or_time',
            new_name='full_day_or_half_day_date_or_late_comming_or_early_logout_time',
        ),
    ]
