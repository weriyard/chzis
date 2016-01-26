from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class CongregationManager(models.Manager):
    def get_by_natural_key(self, congregation_name, *other):
        return self.get(name=congregation_name)


class Congregation(models.Model):
    objects = CongregationManager()

    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)
    circuit = models.IntegerField(null=True, blank=True)
    coordinator = models.ForeignKey('congregation.CongregationMember', models.SET_NULL, related_name='owner', null=True, blank=True, default=None)

    def __unicode__(self):
        return "{name}".format(name=self.name)

    def get_absolute_url(self):
        return "/congregation/{congregation_id}".format(congregation_id=self.id)

    def get_manage_absolute_url(self):
        return "{manage_url}{absolute_url}".format(manage_url=settings.MANAGE_URL, absolute_url=self.get_absolute_url())



class CongregationMember(models.Model):
    user = models.ForeignKey(User)
    congregation = models.ForeignKey(Congregation, null=True, blank=True)
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
    last_modification = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return "{lastname} {firstname}".format(lastname=self.user.last_name, firstname=self.user.first_name)

    def get_absolute_url(self):
        return "/congregations/{congregation_id}/members/{members_id}".format(congregation_id=self.congregation.id if self.congregation is not None else 'unknown',
                                                                             members_id=self.id)

    def get_manage_absolute_url(self):
        return "{manage_url}{absolute_url}".format(manage_url=settings.MANAGE_URL, absolute_url=self.get_absolute_url())

    def get_absolute_url_by_user(self, user_id):
        pass

    class Meta:
        ordering = ['user']


