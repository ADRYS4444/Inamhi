# Generated by Django 5.1.3 on 2024-11-28 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0009_auto_20241126_1457"),
    ]

    operations = [
        migrations.AddField(
            model_name="viaje",
            name="viaticos",
            field=models.FloatField(default=0.0),
        ),
    ]