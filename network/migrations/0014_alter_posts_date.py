# Generated by Django 3.2.4 on 2022-03-15 19:33

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0013_auto_20220313_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 15, 19, 33, 28, 177744, tzinfo=utc)),
        ),
    ]