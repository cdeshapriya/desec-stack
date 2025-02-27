# Generated by Django 5.1.4 on 2024-12-17 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("desecapi", "0043_authenticatedactivateuserwithoverridetokenaction"),
    ]

    operations = [
        migrations.AlterField(
            model_name="captcha",
            name="created",
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name="domain",
            name="renewal_state",
            field=models.IntegerField(
                choices=[(0, "Immortal"), (1, "Fresh"), (2, "Notified"), (3, "Warned")],
                db_index=True,
                default=0,
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="is_active",
            field=models.BooleanField(db_index=True, default=True, null=True),
        ),
        migrations.AddIndex(
            model_name="user",
            index=models.Index(
                fields=["last_login"], name="desecapi_us_last_lo_3b1092_idx"
            ),
        ),
    ]
