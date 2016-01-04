from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class PeopleProfile(models.Model):
    GENDER = (
        ('M', 'male'),
        ('F', 'female'),
    )

    user = models.ForeignKey(User)
    gender = models.CharField(max_length=1, choices=GENDER, default='male')
    default_congregation = models.ForeignKey('congregation.Congregation', models.SET_NULL, null=True, blank=True, default=None)
    last_modification = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return "{lastname} {firstname}".format(lastname=self.user.last_name, firstname=self.user.first_name)

    # class Meta:
    #     ordering = ['last_name', 'first_name']

