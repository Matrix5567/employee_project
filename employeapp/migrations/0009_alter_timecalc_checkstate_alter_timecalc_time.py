# Generated by Django 4.0.5 on 2022-06-20 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employeapp', '0008_timecalc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timecalc',
            name='checkstate',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='timecalc',
            name='time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
