# Generated by Django 2.1 on 2018-11-11 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pc_build', '0008_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='parts',
            field=models.ManyToManyField(blank=True, null=True, to='pc_build.Part'),
        ),
    ]
