# Generated by Django 3.1.14 on 2022-09-25 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atlas', '0003_auto_20220925_1250'),
    ]

    operations = [
        migrations.AddField(
            model_name='atlassettings',
            name='reducedAccuracy',
            field=models.BooleanField(blank=True, default=False, help_text='When showing me on the map, reduce accuracy from zip code level to administrative division (i.e. city/region) level. '),
        ),
    ]
