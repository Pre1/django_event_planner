# Generated by Django 2.1.7 on 2019-02-26 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_event_poster'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='ticket_left',
        ),
        migrations.AlterField(
            model_name='event',
            name='poster',
            field=models.ImageField(null=True, upload_to='event_posters'),
        ),
    ]
