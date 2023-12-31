# Generated by Django 4.2.3 on 2023-07-25 08:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("collect", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="data",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("modelName", models.CharField(max_length=100)),
                ("number", models.IntegerField(default=0)),
                ("game", models.IntegerField(default=0)),
                ("difference", models.IntegerField(default=0)),
                ("BB", models.IntegerField(default=0)),
                ("RB", models.IntegerField(default=0)),
                ("full", models.FloatField(default=0.0)),
                ("BBprobability", models.FloatField(default=0.0)),
                ("RBprobability", models.FloatField(default=0.0)),
            ],
        ),
    ]
