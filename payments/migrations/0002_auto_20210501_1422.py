# Generated by Django 3.2 on 2021-05-01 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='due',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='issued',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
