# Generated by Django 3.0.5 on 2020-07-01 07:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Friend",
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
                    "first_name",
                    models.CharField(max_length=30, verbose_name="first name"),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, null=True, verbose_name="last name"
                    ),
                ),
                ("date_of_birth", models.DateField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="friends",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
