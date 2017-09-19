# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-18 12:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tangodjsforgoodsound', '0012_auto_20170918_0532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dj',
            name='audioformat',
            field=models.CharField(blank=True, choices=[(b'AIFF', 'AIFF Audio Interchange File Format (.aiff, aif)'), (b'WAV', 'WAV Resource Interchange File Format (.wav)'), (b'ADA', 'ADA Advanced Digital Audio (.ada)'), (b'ALAC', 'ALAC Apple Lossless Audio Codec (.m4a, .mp4)'), (b'APE', "APE Monkey's Audio (.ape, .mac)"), (b'FLAC', 'FLAC Free Lossless Audio Codec (.flac, .fla)'), (b'SHN', 'SHN Shorten (.shn)'), (b'TTA', 'TTA The True Audio (.tta)'), (b'WV', 'WV WavPack LOSSLESS (.wv)')], default='', max_length=100, verbose_name='Main audio format'),
        ),
        migrations.AlterField(
            model_name='dj',
            name='audioformatmat2',
            field=models.CharField(blank=True, choices=[(b'AIFF', 'AIFF Audio Interchange File Format (.aiff, aif)'), (b'WAV', 'WAV Resource Interchange File Format (.wav)'), (b'ADA', 'ADA Advanced Digital Audio (.ada)'), (b'ALAC', 'ALAC Apple Lossless Audio Codec (.m4a, .mp4)'), (b'APE', "APE Monkey's Audio (.ape, .mac)"), (b'FLAC', 'FLAC Free Lossless Audio Codec (.flac, .fla)'), (b'SHN', 'SHN Shorten (.shn)'), (b'TTA', 'TTA The True Audio (.tta)'), (b'WV', 'WV WavPack LOSSLESS (.wv)')], default='', max_length=100, verbose_name='Alternative audio format'),
        ),
        migrations.AlterField(
            model_name='dj',
            name='backup_computer',
            field=models.CharField(blank=True, choices=[(b'PCW', 'PC Windows'), (b'PCL', 'PC Linux'), (b'MAC', 'MAC'), (b'MOB', 'Mobile device (Tablet, Smartphone, iPhone, iPad, ...)')], default='', max_length=100, verbose_name='Computer'),
        ),
        migrations.AlterField(
            model_name='dj',
            name='computer',
            field=models.CharField(blank=True, choices=[(b'PCW', 'PC Windows'), (b'PCL', 'PC Linux'), (b'MAC', 'MAC'), (b'MOB', 'Mobile device (Tablet, Smartphone, iPhone, iPad, ...)')], default='', max_length=100, verbose_name='Computer'),
        ),
    ]
