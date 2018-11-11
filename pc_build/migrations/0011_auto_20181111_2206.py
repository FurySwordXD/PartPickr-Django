# Generated by Django 2.1 on 2018-11-11 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pc_build', '0010_shopping_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='parts',
            field=models.ManyToManyField(blank=True, to='pc_build.Part'),
        ),
        migrations.AlterField(
            model_name='shopping_cart',
            name='parts',
            field=models.ManyToManyField(blank=True, to='pc_build.Part'),
        ),
    ]
