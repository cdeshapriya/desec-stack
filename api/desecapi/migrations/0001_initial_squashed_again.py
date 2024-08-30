# Generated by Django 3.1 on 2020-08-25 14:54

import desecapi.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re
import uuid
from django.contrib.postgres.operations import CreateCollation


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        # Explanation: https://adamj.eu/tech/2023/02/23/migrate-django-postgresql-ci-fields-case-insensitive-collation/
        CreateCollation(
            "case_insensitive",
            provider="icu",
            locale="und-u-ks-level2",
            deterministic=False,
        ),
        migrations.CreateModel(
            name="User",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        db_collation="case_insensitive",
                        max_length=254,
                        unique=True,
                        verbose_name="email address",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("is_admin", models.BooleanField(default=False)),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "limit_domains",
                    models.IntegerField(
                        blank=True,
                        default=desecapi.models.User._limit_domains_default,
                        null=True,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Domain",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "name",
                    models.CharField(
                        max_length=191,
                        unique=True,
                        validators=[
                            desecapi.models.validate_lower,
                            django.core.validators.RegexValidator(
                                code="invalid_domain_name",
                                flags=re.RegexFlag["IGNORECASE"],
                                message="Domain names must be labels separated by dots. Labels may consist of up to 63 letters, digits, hyphens, and underscores. The last label may not contain an underscore.",
                                regex="^(([a-z0-9_-]{1,63})\\.)*[a-z0-9-]{1,63}$",
                            ),
                        ],
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="domains",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("published", models.DateTimeField(blank=True, null=True)),
                (
                    "minimum_ttl",
                    models.PositiveIntegerField(
                        default=desecapi.models.Domain._minimum_ttl_default
                    ),
                ),
                ("renewal_changed", models.DateTimeField(auto_now_add=True)),
                (
                    "renewal_state",
                    models.IntegerField(
                        choices=[(1, "Fresh"), (2, "Notified"), (3, "Warned")],
                        default=1,
                    ),
                ),
            ],
            options={
                "ordering": ("created",),
            },
        ),
        migrations.CreateModel(
            name="RRset",
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
                ("touched", models.DateTimeField(auto_now=True)),
                (
                    "subname",
                    models.CharField(
                        blank=True,
                        max_length=178,
                        validators=[
                            desecapi.models.validate_lower,
                            django.core.validators.RegexValidator(
                                code="invalid_subname",
                                message="Subname can only use (lowercase) a-z, 0-9, ., -, and _, may start with a '*.', or just be '*'.",
                                regex="^([*]|(([*][.])?[a-z0-9_.-]*))$",
                            ),
                        ],
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        max_length=10,
                        validators=[
                            desecapi.models.validate_upper,
                            django.core.validators.RegexValidator(
                                code="invalid_type",
                                message="Type must be uppercase alphanumeric and start with a letter.",
                                regex="^[A-Z][A-Z0-9]*$",
                            ),
                        ],
                    ),
                ),
                ("ttl", models.PositiveIntegerField()),
                (
                    "domain",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="desecapi.domain",
                    ),
                ),
            ],
            options={
                "unique_together": {("domain", "subname", "type")},
            },
        ),
        migrations.CreateModel(
            name="AuthenticatedAction",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
            options={
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="AuthenticatedUserAction",
            fields=[
                (
                    "authenticatedaction_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="desecapi.authenticatedaction",
                    ),
                ),
            ],
            options={
                "managed": False,
            },
            bases=("desecapi.authenticatedaction",),
        ),
        migrations.CreateModel(
            name="AuthenticatedDeleteUserAction",
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
            ],
            options={
                "managed": False,
            },
            bases=("desecapi.authenticateduseraction",),
        ),
        migrations.CreateModel(
            name="AuthenticatedResetPasswordUserAction",
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
                ("new_password", models.CharField(max_length=128)),
            ],
            options={
                "managed": False,
            },
            bases=("desecapi.authenticateduseraction",),
        ),
        migrations.CreateModel(
            name="Captcha",
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
                (
                    "content",
                    models.CharField(
                        default=desecapi.models.captcha.captcha_default_content,
                        max_length=24,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Token",
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
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created"),
                ),
                (
                    "key",
                    models.CharField(
                        db_index=True, max_length=128, unique=True, verbose_name="Key"
                    ),
                ),
                (
                    "name",
                    models.CharField(blank=True, max_length=64, verbose_name="Name"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="auth_tokens",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
                ("last_used", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "verbose_name": "Token",
                "verbose_name_plural": "Tokens",
            },
        ),
        migrations.CreateModel(
            name="RR",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("content", models.CharField(max_length=500)),
                (
                    "rrset",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="records",
                        to="desecapi.rrset",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AuthenticatedActivateUserAction",
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
                ("domain", models.CharField(max_length=191)),
            ],
            options={
                "managed": False,
            },
            bases=("desecapi.authenticateduseraction",),
        ),
        migrations.CreateModel(
            name="AuthenticatedChangeEmailUserAction",
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
                ("new_email", models.EmailField(max_length=254)),
            ],
            options={
                "managed": False,
            },
            bases=("desecapi.authenticateduseraction",),
        ),
        migrations.CreateModel(
            name="AuthenticatedBasicUserAction",
            fields=[
                (
                    "authenticatedaction_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="desecapi.authenticatedaction",
                    ),
                ),
            ],
            options={
                "managed": False,
            },
            bases=("desecapi.authenticatedaction",),
        ),
        migrations.CreateModel(
            name="AuthenticatedDomainBasicUserAction",
            fields=[
                (
                    "authenticatedbasicuseraction_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="desecapi.authenticatedbasicuseraction",
                    ),
                ),
            ],
            options={
                "managed": False,
            },
            bases=("desecapi.authenticatedbasicuseraction",),
        ),
        migrations.CreateModel(
            name="AuthenticatedRenewDomainBasicUserAction",
            fields=[
                (
                    "authenticateddomainbasicuseraction_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="desecapi.authenticateddomainbasicuseraction",
                    ),
                ),
            ],
            options={
                "managed": False,
            },
            bases=("desecapi.authenticateddomainbasicuseraction",),
        ),
        migrations.CreateModel(
            name="Donation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        default=desecapi.models.Donation._created_default
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("iban", models.CharField(max_length=34)),
                ("bic", models.CharField(max_length=11)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=8)),
                ("message", models.CharField(blank=True, max_length=255)),
                (
                    "due",
                    models.DateTimeField(default=desecapi.models.Donation._due_default),
                ),
                (
                    "mref",
                    models.CharField(
                        default=desecapi.models.Donation._mref_default, max_length=32
                    ),
                ),
                ("email", models.EmailField(blank=True, max_length=255)),
            ],
            options={
                "ordering": ("created",),
                "managed": False,
            },
        ),
    ]
