# Generated by Django 4.1.3 on 2023-01-27 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_comments_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]