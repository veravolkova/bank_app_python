# Generated by Django 2.1 on 2018-08-07 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restservice', '0005_transfer_transaction_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='mercant_city',
            field=models.CharField(default='LOS ANGELES', max_length=20),
        ),
        migrations.AddField(
            model_name='transaction',
            name='mercant_country',
            field=models.CharField(default='US', max_length=10),
        ),
        migrations.AddField(
            model_name='transaction',
            name='mercant_name',
            field=models.CharField(default='SNEAKERS R US', max_length=100),
        ),
    ]
