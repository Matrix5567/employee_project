# Generated by Django 4.0.5 on 2022-06-17 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employeapp', '0002_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='role',
            field=models.CharField(blank=True, choices=[('User', 'User'), ('Admin', 'Admin')], max_length=50, null=True),
        ),
    ]
