# Generated by Django 2.1.7 on 2019-02-26 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_auto_20190226_0900'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='poster',
            field=models.ImageField(default='events/static/img/01.jpg', upload_to='event_posters'),
        ),
    ]
