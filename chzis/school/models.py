# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.core import exceptions

from chzis.congregation.models import CongregationMember
from chzis.meetings.models import MeetingItem, MeetingTask


class Lesson(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=255)
    reading = models.BooleanField(default=False)
    demo = models.BooleanField(default=False)
    discourse = models.BooleanField(default=False)
    book_page = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    last_modification = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __unicode__(self):
        return "{number} {name}".format(number=self.number, name=self.name)

    class Meta:
        ordering = ['number']


class Background(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)
    last_modification = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return "{number} {name}".format(number=self.number, name=self.name)

    class Meta:
        ordering = ['number']


class SchoolTask(models.Model):
    task = models.ForeignKey(MeetingTask, null=True, blank=True)
    lesson = models.ForeignKey(Lesson)
    lesson_passed = models.NullBooleanField(null=True, blank=True)
    lesson_passed_date = models.DateTimeField(auto_now=True, null=True)
    background = models.ForeignKey(Background, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    last_modification = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return "{number}".format(number=self.id)

    def get_absolute_url(self):
        return "/school/tasks/{id}".format(id=self.id)

    class Meta:
        permissions = (
                    ("can_view_all_tasks", "Can see all available tasks"),
                    ("can_judge_tasks", "Can judge presented tasks by popele"),
                )
