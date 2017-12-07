# -*- coding: utf-8 -*-
# Manually create non-existing approval objects


from __future__ import unicode_literals

from django.db import migrations


def forwards_func(apps, schema_editor):
    Alumni = apps.get_model("alumni", "Alumni")
    Approval = apps.get_model("alumni", "Approval")

    db_alias = schema_editor.connection.alias
    for instance in Alumni.objects.using(db_alias).all():
        Approval.objects.using(db_alias).get_or_create(member=instance,
                                                       defaults={
                                                           'gsuite': None,
                                                           'approval': False
                                                       })


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('alumni', '0001_initial'),
        ('alumni', '0002_alumni_resetexistingemailpassword'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
