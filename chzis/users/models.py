from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class PeopleProfile(models.Model):
    GENDER = (
        ('M', 'male'),
        ('F', 'female'),
    )

    user = models.OneToOneField(User, related_name="profile")
    gender = models.CharField(max_length=1, choices=GENDER, default='male')
    default_congregation = models.ForeignKey('congregation.Congregation', models.SET_NULL, null=True, blank=True, default=None)
    birth_date = models.DateTimeField(null=True, blank=True)
    baptism_date = models.DateField(null=True, blank=True)
    last_modification = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return "ss{lastname} {firstname}".format(lastname=self.user.last_name, firstname=self.user.first_name)

    # class Meta:
    #     ordering = ['last_name', 'first_name']

