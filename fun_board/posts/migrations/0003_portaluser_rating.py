# Generated by Django 4.1.3 on 2023-01-26 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_posts_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='portaluser',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
