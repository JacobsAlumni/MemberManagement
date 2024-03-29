# Generated by Django 3.1.14 on 2022-09-08 13:43

from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('donation_receipts', '0010_auto_20201129_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donationreceipt',
            name='amount_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('EUR', 'Euro'), ('USD', 'US Dollar')], default='EUR', editable=False, max_length=3),
        ),
    ]
