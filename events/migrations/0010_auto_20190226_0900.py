# Generated by Django 2.1.7 on 2019-02-26 09:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_auto_20190226_0850'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='date',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='time',
        ),
        migrations.AddField(
            model_name='booking',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2019, 2, 26, 9, 0, 0, 342394, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
