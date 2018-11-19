# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-02 23:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osf', '0043_auto_20170828_0734'),
    ]

    operations = [
        migrations.CreateModel(
            name='SwiftFileNode',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('osf.basefilenode',),
        ),
        migrations.AlterField(
            model_name='basefilenode',
            name='type',
            field=models.CharField(choices=[('osf.trashedfilenode', 'trashed file node'), ('osf.trashedfile', 'trashed file'), ('osf.trashedfolder', 'trashed folder'), ('osf.osfstoragefilenode', 'osf storage file node'), ('osf.osfstoragefile', 'osf storage file'), ('osf.osfstoragefolder', 'osf storage folder'), ('osf.boxfilenode', 'box file node'), ('osf.boxfolder', 'box folder'), ('osf.boxfile', 'box file'), ('osf.dataversefilenode', 'dataverse file node'), ('osf.dataversefolder', 'dataverse folder'), ('osf.dataversefile', 'dataverse file'), ('osf.dropboxfilenode', 'dropbox file node'), ('osf.dropboxfolder', 'dropbox folder'), ('osf.dropboxfile', 'dropbox file'), ('osf.figsharefilenode', 'figshare file node'), ('osf.figsharefolder', 'figshare folder'), ('osf.figsharefile', 'figshare file'), ('osf.githubfilenode', 'github file node'), ('osf.githubfolder', 'github folder'), ('osf.githubfile', 'github file'), ('osf.googledrivefilenode', 'google drive file node'), ('osf.googledrivefolder', 'google drive folder'), ('osf.googledrivefile', 'google drive file'), ('osf.owncloudfilenode', 'owncloud file node'), ('osf.owncloudfolder', 'owncloud folder'), ('osf.owncloudfile', 'owncloud file'), ('osf.s3filenode', 's3 file node'), ('osf.s3folder', 's3 folder'), ('osf.s3file', 's3 file'), ('osf.swiftfilenode', 'swift file node'), ('osf.swiftfolder', 'swift folder'), ('osf.swiftfile', 'swift file')], db_index=True, max_length=255),
        ),
        migrations.CreateModel(
            name='SwiftFile',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('osf.swiftfilenode', models.Model),
        ),
        migrations.CreateModel(
            name='SwiftFolder',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('osf.swiftfilenode', models.Model),
        ),
    ]