# Generated by Django 4.2.2 on 2023-07-06 06:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_alter_product_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='sale_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]