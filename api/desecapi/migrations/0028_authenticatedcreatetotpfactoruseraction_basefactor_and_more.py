# Generated by Django 4.1 on 2022-08-23 22:23

import desecapi.models.mfa
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("desecapi", "0027_user_credentials_changed"),
    ]

    operations = [
        migrations.CreateModel(
            name="AuthenticatedCreateTOTPFactorUserAction",
            fields=[
                (
                    "authenticateduseraction_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="desecapi.authenticateduseraction",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=64)),
            ],
            options={
                "managed": False,
            },
            bases=("desecapi.authenticateduseraction",),
        ),
        migrations.CreateModel(
            name="BaseFactor",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("last_used", models.DateTimeField(blank=True, null=True)),
                ("name", models.CharField(blank=True, default="", max_length=64)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TOTPFactor",
            fields=[
                (
                    "basefactor_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="desecapi.basefactor",
                    ),
                ),
                (
                    "secret",
                    models.BinaryField(
                        default=desecapi.models.mfa.TOTPFactor._secret_default,
                        max_length=32,
                    ),
                ),
                ("last_verified_timestep", models.PositiveIntegerField(default=0)),
            ],
            bases=("desecapi.basefactor",),
        ),
        migrations.AddConstraint(
            model_name="basefactor",
            constraint=models.UniqueConstraint(
                fields=("user", "name"), name="unique_user_name"
            ),
        ),
    ]
