# Generated by Django 2.2.1 on 2021-01-19 16:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0003_auto_20210109_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 19, 20, 7, 0, 233738)),
        ),
    ]