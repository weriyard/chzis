# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

from chzis.congregation.models import Congregation


class MeetingType(models.Model):
    name = models.CharField(max_length=255)
    duration = models.IntegerField(null=True, blank=True)
    week_day = models.IntegerField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    congregation = models.ForeignKey(Congregation, null=True, blank=True)

    def __unicode__(self):
        return "{name}".format(name=self.name)


class MeetingPart(models.Model):
    name = models.CharField(max_length=255)
    type = models.ForeignKey(MeetingType)
    duration = models.IntegerField()
    order = models.IntegerField()

    def __unicode__(self):
        return "{name}".format(name=self.name)


class MeetingItem(models.Model):
    name = models.CharField(max_length=255)
    duration = models.IntegerField()
    part = models.ForeignKey(MeetingPart)
    order = models.IntegerField()

    def __unicode__(self):
        return "{name}".format(name=self.name)
