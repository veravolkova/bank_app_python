# Generated by Django 2.1 on 2018-08-04 13:15

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Balance')),
                ('currency', models.PositiveIntegerField(choices=[(0, 'EUR'), (1, 'USD'), (2, 'GBP'), (3, 'RUB')], default=0, verbose_name='Currency')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Create time')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Create time')),
                ('destination_account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='destination_account', to='restservice.Account', verbose_name='Destination Account')),
                ('source_account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='source_account', to='restservice.Account', verbose_name='Source Account')),
            ],
        ),
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Create time')),
            ],
        ),
    ]
