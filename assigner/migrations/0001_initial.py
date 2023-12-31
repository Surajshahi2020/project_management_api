# Generated by Django 4.2.3 on 2023-08-02 05:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("slug", models.SlugField(blank=True, null=True, unique=True)),
                ("full_name", models.CharField(max_length=255)),
                (
                    "phone",
                    models.CharField(blank=True, max_length=10, null=True, unique=True),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True,
                        max_length=254,
                        null=True,
                        unique=True,
                        verbose_name="email address",
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[("M", "MALE"), ("F", "FEMALE"), ("O", "OTHER")],
                        default="M",
                        max_length=1,
                    ),
                ),
                ("date_of_birth", models.DateField(blank=True, null=True)),
                ("profile_pic", models.URLField(blank=True, max_length=500, null=True)),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("SA", "SUPERADMIN"),
                            ("A", "ADMIN"),
                            ("U", "USER"),
                            ("SU", "SUPERVISOR"),
                            ("HR", "HUMAN_RESOURCE"),
                        ],
                        default="U",
                        max_length=2,
                    ),
                ),
                ("joined_date", models.DateTimeField(auto_now_add=True)),
                ("is_active", models.BooleanField(default=True)),
                ("is_blocked", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name": "User",
                "verbose_name_plural": "All Users",
                "db_table": "user",
            },
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="Created at"
                    ),
                ),
                (
                    "modified_at",
                    models.DateTimeField(
                        auto_now=True, db_index=True, verbose_name="Last modified at"
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField()),
                (
                    "status",
                    models.CharField(
                        choices=[("D", "Draft"), ("O", "Ongoing"), ("C", "Completed")],
                        default="D",
                        max_length=1,
                    ),
                ),
                (
                    "contributors",
                    models.ManyToManyField(
                        related_name="contributed_projects", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(app_label)s_%(class)s_creator",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created by",
                    ),
                ),
                (
                    "modifier",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(app_label)s_%(class)s_modifier",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Modified_by",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="Created at"
                    ),
                ),
                (
                    "modified_at",
                    models.DateTimeField(
                        auto_now=True, db_index=True, verbose_name="Last modified at"
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("description", models.TextField()),
                (
                    "status",
                    models.CharField(
                        choices=[("D", "Draft"), ("O", "Ongoing"), ("C", "Completed")],
                        default="D",
                        max_length=1,
                    ),
                ),
                (
                    "assignee",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="assigned_tasks",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(app_label)s_%(class)s_creator",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created by",
                    ),
                ),
                (
                    "modifier",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(app_label)s_%(class)s_modifier",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Modified_by",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tasks",
                        to="assigner.project",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="SubmittedTask",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="Created at"
                    ),
                ),
                (
                    "modified_at",
                    models.DateTimeField(
                        auto_now=True, db_index=True, verbose_name="Last modified at"
                    ),
                ),
                ("submission_date", models.DateTimeField(auto_now_add=True)),
                ("is_approved", models.BooleanField(default=False)),
                ("remarks", models.TextField(blank=True, null=True)),
                (
                    "creator",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(app_label)s_%(class)s_creator",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created by",
                    ),
                ),
                (
                    "modifier",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(app_label)s_%(class)s_modifier",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Modified_by",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="submitted_tasks",
                        to="assigner.project",
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="submitted_tasks",
                        to="assigner.task",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
