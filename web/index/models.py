# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


class ScanTask(models.Model):
    task_name = models.CharField(max_length=50)
    target = models.CharField(max_length=50)
    target_type = models.CharField(max_length=30)
    task_tag = models.CharField(max_length=100)
    last_scan_time = models.DateTimeField()
    is_active = models.BooleanField(default=False)


class BanList(models.Model):
    ban_name = models.CharField(max_length=50)
    ban_domain = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)

