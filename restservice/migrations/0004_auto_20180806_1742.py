# Generated by Django 2.1 on 2018-08-06 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restservice', '0003_auto_20180806_1056'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='balance',
        ),
        migrations.AddField(
            model_name='account',
            name='available_balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Available balance'),
        ),
        migrations.AddField(
            model_name='account',
            name='ledger_balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Ledger balance'),
        ),
    ]
