# Generated by Django 2.1 on 2018-08-07 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restservice', '0008_auto_20180807_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Transaction Amount'),
        ),
    ]
