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
        return "{name}".format(name=self.name)

    def get_absolute_url(self):
        return "/school/lesson/{id}".format(id=self.id)

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
    subordinate = models.ForeignKey(CongregationMember, null=True, blank=True, related_name='subordinate_person')
    lesson = models.ForeignKey(Lesson)
    lesson_passed = models.NullBooleanField(null=True, blank=True)
    lesson_passed_date = models.DateTimeField(blank=True, null=True)
    creator = models.ForeignKey(CongregationMember, null=True, blank=True, related_name='creator_person')
    supervisor = models.ForeignKey(CongregationMember, null=True, blank=True, related_name='supervisor_person')
    background = models.ForeignKey(Background, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    last_modification = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return "{number}".format(number=self.id)

    def get_absolute_url(self):
        return "/school/tasks/{id}".format(id=self.task.id)

    def delete(self, *args, **kwargs):
        try:
            MeetingTask.objects.get(id=self.task.id).delete()
        except exceptions.ObjectDoesNotExist:
            super(SchoolTask, self).delete( *args, **kwargs)

    class Meta:
        permissions = (
            ("can_view_all_tasks", "Can see all available tasks"),
            ("can_judge_tasks", "Can judge presented tasks by popele"),
        )
