# Generated by Django 3.0.5 on 2020-07-09 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("trading_bot", "0004_auto_20200709_1344"),
    ]

    operations = [
        migrations.AddField(
            model_name="bot", name="lock_time", field=models.IntegerField(default=12),
        ),
    ]