# Generated by Django 2.1 on 2018-11-11 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pc_build', '0011_auto_20181111_2206'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
