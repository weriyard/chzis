from __future__ import unicode_literals

from django.db import models

class Congregation(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True)
    number = models.IntegerField(null=True)
    circuit = models.IntegerField(null=True)
    coordinator = models.ForeignKey('congregation.CongregationMember', models.SET_NULL, related_name='owner', null=True, blank=True, default=None)


class CongregationMember(models.Model):
    user = models.ForeignKey('users.People')
    congregation = models.ForeignKey(Congregation, null=True, blank=True)
    age = models.IntegerField(null=True)
    baptism_date = models.DateField(null=True)
    active = models.BooleanField(default=False)
    servant = models.BooleanField(default=False)
    elder = models.BooleanField(default=False)
    coordinator = models.BooleanField(default=False)
    pioneer = models.BooleanField(default=False)
    school_allow = models.BooleanField(default=False)
    master = models.BooleanField(default=False)
    slave = models.BooleanField(default=False)
    reader_only = models.BooleanField(default=False)
    lector = models.BooleanField(default=False)
    sound_sysop = models.BooleanField(default=False)
    last_modification = models.DateTimeField(auto_now=True)



