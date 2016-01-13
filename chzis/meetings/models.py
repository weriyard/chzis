# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

from chzis.congregation.models import Congregation, CongregationMember


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


#TODO: dodac nr weekendu w ktory dany punkt jest, sprawdzic czy zawsze to jest 1 tydzien
class MeetingItem(models.Model):
    name = models.CharField(max_length=255)
    duration = models.IntegerField()
    part = models.ForeignKey(MeetingPart)
    order = models.IntegerField()

    def __unicode__(self):
        return "{name}".format(name=self.name)


class MeetingTask(models.Model):
    meeting_item = models.ForeignKey(MeetingItem)
    topic = models.CharField(max_length=255,null=True, blank=True)
    person = models.ForeignKey(CongregationMember)
    creation_date = models.DateField(auto_now=True)
    presentation_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    last_modification = models.DateTimeField(auto_now=True, null=True)
