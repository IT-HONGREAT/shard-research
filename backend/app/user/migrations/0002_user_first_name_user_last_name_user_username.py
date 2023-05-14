# Generated by Django 4.1.4 on 2023-05-14 17:10

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="first_name",
            field=models.CharField(blank=True, max_length=150, verbose_name="first name"),
        ),
        migrations.AddField(
            model_name="user",
            name="last_name",
            field=models.CharField(blank=True, max_length=150, verbose_name="last name"),
        ),
        migrations.AddField(
            model_name="user",
            name="username",
            field=models.CharField(
                default="",
                error_messages={"unique": "A user with that username already exists."},
                help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                max_length=150,
                unique=True,
                validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
                verbose_name="username",
            ),
            preserve_default=False,
        ),
    ]