# Generated by Django 4.2.4 on 2023-08-05 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("donations", "0007_auto_20220908_1343"),
    ]

    operations = [
        migrations.AlterField(
            model_name="donation",
            name="target",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={"active": True},
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="donations.donationtarget",
                verbose_name="Donating towards",
            ),
        ),
    ]
