# Generated by Django 4.2.3 on 2023-08-01 01:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("collect", "0002_data"),
    ]

    operations = [
        migrations.RenameField(
            model_name="data",
            old_name="full",
            new_name="allprobability",
        ),
        migrations.AddField(
            model_name="data",
            name="date",
            field=models.DateField(default=datetime.date(1111, 1, 1)),
        ),
    ]