# Generated by Django 5.0.6 on 2024-06-17 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("desecapi", "0037_remove_tokendomainpolicy_perm_dyndns"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="throttle_daily_rate",
            field=models.PositiveIntegerField(null=True),
        ),
    ]
