# Generated by Django 4.1.5 on 2023-01-11 09:32

from django.db import migrations
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="baseuser",
            managers=[
                ("objects", users.models.UserManager()),
            ],
        ),
    ]
