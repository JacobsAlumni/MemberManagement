# Generated by Django 3.1.14 on 2022-08-20 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0003_auto_20220818_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='completed',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
