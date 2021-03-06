# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-30 18:34
from __future__ import unicode_literals

import logging

from django.apps import apps
from django.db import migrations, models

from addons.osfstorage.models import NodeSettings, Region
from addons.osfstorage.settings import DEFAULT_REGION_ID, DEFAULT_REGION_NAME

logger = logging.getLogger(__name__)
osfstorage_config = apps.get_app_config('addons_osfstorage')

class Migration(migrations.Migration):

    # Avoid locking the addons_osfstorage_nodesettings table
    atomic = False

    dependencies = [
        ('osf', '0102_merge_20180509_0846'),
    ]

    def add_default_region_to_nodesettings(self, *args, **kwargs):
        default_region, created = Region.objects.get_or_create(
            _id=DEFAULT_REGION_ID,
            name=DEFAULT_REGION_NAME,
        )
        if created:
            logger.info('Created default region: {}'.format(DEFAULT_REGION_NAME))
        BATCHSIZE = 5000

        max_pk = NodeSettings.objects.aggregate(models.Max('pk'))['pk__max']
        if max_pk is not None:
            for offset in range(0, max_pk + 1, BATCHSIZE):
                (NodeSettings.objects
                 .filter(pk__gte=offset)
                 .filter(pk__lt=offset + BATCHSIZE)
                 .filter(region__isnull=True)
                 .update(region=default_region))
                logger.info(
                    'Updated addons_osfstorage_nodesettings {}-{}/{}'.format(
                        offset,
                        offset + BATCHSIZE,
                        max_pk,
                    )
                )

    def unset_default_region(self, *args, **kwargs):
        BATCHSIZE = 5000

        max_pk = NodeSettings.objects.aggregate(models.Max('pk'))['pk__max']
        if max_pk is not None:
            for offset in range(0, max_pk + 1, BATCHSIZE):
                (NodeSettings.objects
                 .filter(pk__gte=offset)
                 .filter(pk__lt=offset + BATCHSIZE)
                 .filter(region__isnull=False)
                 .update(region=None))
                logger.info(
                    'Unset addons_osfstorage_nodesettings {}-{}/{}'.format(
                        offset,
                        offset + BATCHSIZE,
                        max_pk,
                    )
                )

    operations = [
        migrations.RunPython(add_default_region_to_nodesettings, unset_default_region),
    ]
