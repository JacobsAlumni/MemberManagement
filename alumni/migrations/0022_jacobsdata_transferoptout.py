# Generated by Django 4.2.4 on 2023-12-21 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("alumni", "0021_approval_autocreated"),
    ]

    operations = [
        migrations.AddField(
            model_name="jacobsdata",
            name="transferOptout",
            field=models.BooleanField(
                default=False,
                help_text="person has opted out of data transfer to the university. ",
            ),
        ),
    ]
