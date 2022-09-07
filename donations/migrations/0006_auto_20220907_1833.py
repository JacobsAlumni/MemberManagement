# Generated by Django 3.1.14 on 2022-09-07 18:33

from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0005_auto_20220906_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='amount',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default_currency='EUR', help_text='Use "," as the decimal separator, i.e. "1.000,23" means 1000 Euros and 23 Cents. ', max_digits=10),
        ),
    ]
