from __future__ import unicode_literals
from django.db import models
import datetime
from chzis.congregation.models import CongregationMember


class Lesson(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=255)
    reading = models.BooleanField(default=False)
    demo = models.BooleanField(default=False)
    discourse = models.BooleanField(default=False)
    book_page = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    last_modification = models.DateTimeField(default=datetime.datetime.now())

    def __unicode__(self):
        return "{number} {name}".format(number=self.number, name=self.name)

    class Meta:
        ordering = ['number']

class Background(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)
    last_modification = models.DateTimeField(default=datetime.datetime.now())

    def __unicode__(self):
        return "{number} {name}".format(number=self.number, name=self.name)

    class Meta:
        ordering = ['number']


class StudentProfile(models.Model):
    topic = models.CharField(max_length=255)
    person = models.ForeignKey(CongregationMember)
    lesson = models.ForeignKey(Lesson)
    background = models.ForeignKey(Background)
    presentation_date = models.DateField(auto_now=True)
    lesson_passed = models.BooleanField(default=False)
    lesson_comments = models.TextField(null=True)
    description = models.TextField(null=True)
    creation_date = models.DateField(auto_now=True)
    last_modification = models.DateTimeField(default=datetime.datetime.now())

