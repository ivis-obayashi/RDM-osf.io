# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-02 19:38
from __future__ import unicode_literals

from django.db import migrations
from django.core.management import call_command


def add_reviews_notification_subscription(state, schema_editor):
    call_command('add_notification_subscription', '--notification=global_reviews', state=state)

class Migration(migrations.Migration):

    dependencies = [
        ('osf', '0060_reviews'),
    ]

    operations = [
        migrations.RunPython(add_reviews_notification_subscription),
    ]
