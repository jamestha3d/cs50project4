# Generated by Django 3.2.4 on 2022-03-23 13:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0016_alter_posts_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 23, 13, 49, 40, 544985, tzinfo=utc)),
        ),
    ]