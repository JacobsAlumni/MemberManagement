# Generated by Django 2.2.13 on 2020-11-09 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation_receipts', '0006_donationreceipt_finalized'),
    ]

    operations = [
        migrations.AddField(
            model_name='donationreceipt',
            name='internal_notes',
            field=models.TextField(blank=True),
        ),
    ]
