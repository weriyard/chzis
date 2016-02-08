# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.core import exceptions

from chzis.congregation.models import Congregation, CongregationMember
from django.utils.translation import ugettext_lazy as _


class MeetingTypeManager(models.Manager):
    def get_by_natural_key(self, meeting_type, *other):
        return self.filter(name=meeting_type)[0]


class MeetingType(models.Model):
    objects = MeetingTypeManager()

    name = models.CharField(max_length=255)
    duration = models.IntegerField(null=True, blank=True)
    week_day = models.IntegerField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    congregation = models.ForeignKey(Congregation, null=True, blank=True)

    def __unicode__(self):
        return "{name} ({start_time})".format(name=self.name, start_time=self.start_time)


class MeetingPartManager(models.Manager):
    def get_by_natural_key(self, meeting_part, *other):
        return self.get(name=meeting_part)


class MeetingPart(models.Model):
    objects = MeetingPartManager()

    name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    type = models.ForeignKey(MeetingType)
    duration = models.IntegerField()
    order = models.IntegerField()

    def __unicode__(self):
        return "{type} - {full_name} ".format(type=self.type.name, full_name=self.full_name)


class MeetingItem(models.Model):
    name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    duration = models.IntegerField(null=True, blank=True)
    part = models.ForeignKey(MeetingPart)
    weekend = models.IntegerField(null=True, blank=True)
    order = models.IntegerField()

    def __unicode__(self):
        return "[{type}] {part} - {full_name}".format(type=self.part.type.name, part=self.part.full_name, full_name=self.full_name)

    class Meta:
        ordering = ['part__type__name','part__order', 'order']


class MeetingTask(models.Model):
    meeting_item = models.ForeignKey(MeetingItem)
    topic = models.CharField(max_length=255,null=True, blank=True)
    person = models.ForeignKey(CongregationMember)
    creation_date = models.DateField(auto_now=True)
    presentation_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    last_modification = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return "{id} {meeting} {person} {presentation_date}".format(id=self.id,
                                                                    meeting=self.meeting_item,
                                                                    person=self.person,
                                                                    presentation_date=self.presentation_date)

