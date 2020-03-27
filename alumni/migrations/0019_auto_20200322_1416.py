# Generated by Django 2.2.11 on 2020-03-22 14:16

import alumni.fields.country
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumni', '0018_auto_20200210_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumni',
            name='nationality',
            field=alumni.fields.country.CountryField(help_text='You can select multiple options by holding the <em>Ctrl</em> key (or <em>Command</em> on Mac) while clicking', max_length=749, multiple=True),
        ),
    ]