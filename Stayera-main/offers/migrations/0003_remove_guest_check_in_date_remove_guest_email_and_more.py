# Generated by Django 5.2 on 2025-04-14 17:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0002_guest_room_remove_ticketoffer_booked_count_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guest',
            name='check_in_date',
        ),
        migrations.RemoveField(
            model_name='guest',
            name='email',
        ),
        migrations.RemoveField(
            model_name='guest',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='guest',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='guest',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='guest',
            name='name',
            field=models.CharField(default=101, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='booking',
            name='guest',
            field=models.ForeignKey(default=101, on_delete=django.db.models.deletion.CASCADE, to='offers.guest'),
            preserve_default=False,
        ),
    ]
