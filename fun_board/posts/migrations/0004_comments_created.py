# Generated by Django 4.1.3 on 2023-01-27 10:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_portaluser_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 27, 10, 39, 42, 479058, tzinfo=datetime.timezone.utc)),
        ),
    ]