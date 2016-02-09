from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from chzis.users.models import PeopleProfile


class CongregationManager(models.Manager):
    def get_by_natural_key(self, congregation_name, *other):
        return self.get(name=congregation_name)


class Congregation(models.Model):
    objects = CongregationManager()

    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)
    circuit = models.IntegerField(null=True, blank=True)
    coordinator = models.ForeignKey('congregation.CongregationMember', models.SET_NULL, related_name='owner', null=True,
                                    blank=True, default=None)

    def __unicode__(self):
        return "{name}".format(name=self.name)

    def get_absolute_url(self):
        return "/congregations/{congregation_id}".format(congregation_id=self.id)

    def get_manage_absolute_url(self):
        return "{manage_url}{absolute_url}".format(manage_url=settings.MANAGE_URL, absolute_url=self.get_absolute_url())


class CongregationMemberManager(models.Manager):
    def get_by_natural_key(self, congregation_member, *other):
        return self.get(user__username=congregation_member)


class CongregationMember(models.Model):
    objects = CongregationMemberManager()

    user = models.ForeignKey(User)
    congregation = models.ForeignKey(Congregation, null=True, blank=True)
    active = models.BooleanField(default=False)
    last_modification = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return "{lastname} {firstname}".format(lastname=self.user.last_name, firstname=self.user.first_name)

    def get_absolute_url(self):
        return "/congregations/{congregation_id}/members/{members_id}".format(
            congregation_id=self.congregation.id if self.congregation is not None else 'unknown',
            members_id=self.id)

    @property
    def member_fullname(self):
        return "{firstname} {lastname}".format(firstname=self.user.first_name,
                                               lastname=self.user.last_name)

    class Meta:
        ordering = ['user']
        permissions = (
            ("can_manage", "Can manage"),
        )


class CongregationPrivilegesManager(models.Manager):
    def get_by_natural_key(self, privilege_name, *other):
        return self.get(name=privilege_name)


class CongregationPrivileges(models.Model):
    objects = CongregationPrivilegesManager()

    GENDER = (
        ('M', 'male'),
        ('F', 'female'),
        ('A', 'all')
    )

    name = models.CharField(max_length=255, null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    allow_gender = models.CharField(max_length=1, choices=PeopleProfile.GENDER, default='all')
    description = description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return "{name} ({full_name})".format(name=self.name, full_name=self.full_name)


class CongregationMemberPrivileges(models.Model):
    member = models.ForeignKey(CongregationMember, null=True, blank=True)
    privilege = models.ForeignKey(CongregationPrivileges, null=True, blank=True)

    def save(self, *args, **kwargs):
        member_gender = self.member.user.profile.gender
        if self.privilege.allow_gender != 'A' and member_gender != self.privilege.allow_gender:
            raise RuntimeError

        super(CongregationMemberPrivileges, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{member_name} ({privlege_name})".format(member_name=self.member.user.username,
                                                        privlege_name=self.privilege.full_name)
