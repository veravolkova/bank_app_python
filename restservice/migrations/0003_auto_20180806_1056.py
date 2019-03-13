# Generated by Django 2.1 on 2018-08-06 09:56

from django.db import migrations, models
import restservice.utils


class Migration(migrations.Migration):

    dependencies = [
        ('restservice', '0002_auto_20180804_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='id',
            field=models.IntegerField(default=restservice.utils.get_random_id, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='id',
            field=models.IntegerField(default=restservice.utils.get_random_id, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='type',
            field=models.PositiveIntegerField(choices=[(0, 'AUTH'), (1, 'PRSNT')], default=0, verbose_name='Message'),
        ),
        migrations.AlterField(
            model_name='transfer',
            name='id',
            field=models.IntegerField(default=restservice.utils.get_random_id, editable=False, primary_key=True, serialize=False),
        ),
    ]