# Generated by Django 3.1.14 on 2022-08-18 19:53

from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='amount',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default_currency='EUR', max_digits=5),
        ),
        migrations.AddField(
            model_name='donation',
            name='amount_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('EUR', 'Euro')], default='EUR', editable=False, max_length=3),
        ),
        migrations.AlterField(
            model_name='donation',
            name='target',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='donations.donationtarget', verbose_name='Donating towards'),
        ),
    ]