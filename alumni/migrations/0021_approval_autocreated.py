# Generated by Django 3.1.12 on 2021-06-11 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumni', '0020_auto_20200412_1210'),
    ]

    operations = [
        migrations.AddField(
            model_name='approval',
            name='autocreated',
            field=models.BooleanField(default=False, help_text='Has the user been automatically created?'),
        ),
    ]
